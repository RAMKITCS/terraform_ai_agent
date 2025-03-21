import os
import logging
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from io import BytesIO

# Load environment variables securely
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    st.error("❌ Missing OpenAI API Key!\n\n💡 Create a `.env` file and add `OPENAI_API_KEY=<YOUR_API_KEY>`.")
    st.stop()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logging.info("Starting code generation process...")

# Initialize OpenAI model
llm = ChatOpenAI(
    model_name="gpt-4o",
    openai_api_key=openai_api_key,
    temperature=0.1,
    max_retries=3
)

# Session state for refinement
if "refinement_iteration" not in st.session_state:
    st.session_state.refinement_iteration = 0

# Dynamic dropdown values with option to add custom services
default_services = {
    "AWS": ["EC2", "S3", "RDS", "EKS", "Load Balancer", "Firewall"],
    "Azure": ["Virtual Machines", "AKS", "Blob Storage", "SQL Database", "Firewall"],
    "GCP": ["Compute Engine", "GKE", "Cloud Storage", "Cloud SQL", "Firewall"]
}

if "custom_services" not in st.session_state:
    st.session_state.custom_services = {provider: [] for provider in default_services}

# Utility function for safe model invocation
def safe_invoke(prompt):
    try:
        response = llm.invoke(prompt)
        return response.content.strip() if hasattr(response, 'content') else str(response).strip() if response else "❌ No response received!"
    except Exception as e:
        logging.error(f"Error in code generation: {e}")
        st.error(f"❌ Error generating configuration: {str(e)}")
        return None

# Function to refine Terraform code
def refine_code(feedback, existing_code, cloud_provider, service):
    prompt = f"""
    Refine the following Terraform configuration based on this user feedback:

    Feedback: {feedback}

    Configuration:
    {existing_code}

    Ensure the output remains structured, clean, and easy to read.
    Ensure variables are defined only in `variables.tf` and referenced in `main.tf`.
    Separate the provider block into `provider.tf`.
    Improve security, efficiency, maintainability, and follow best practices.
    Output only the updated configuration.
    """
    return safe_invoke(prompt)

# Function to generate modular Terraform code
def generate_code(cloud_provider, service, include_modules, include_rego):
    prompts = {
        "provider": f"""
        Create a Terraform `provider.tf` file for {service} on {cloud_provider}.
        Ensure the provider block follows best practices with dynamic region and authentication details.
        """,
        "variables": f"""
        Create a Terraform `variables.tf` file for {service} on {cloud_provider}.
        Include key variables like region, instance type, and scaling configurations.
        Follow naming conventions and add meaningful descriptions for all variables.
        Do NOT include any resource blocks here.
        """,
        "main": f"""
        Create a Terraform `main.tf` file for {service} on {cloud_provider}.
        Reference variables from `variables.tf` instead of defining them here.
        Exclude provider block (which should be in `provider.tf`).
        Include clear resource blocks with appropriate tags, encryption settings, and IAM roles.
        Follow best practices for modularization, security, and scalability.
        """,
        "backend": f"""
        Create a Terraform `backend.tf` file for {service} on {cloud_provider}.
        Include recommended configurations for remote state storage such as AWS S3 with DynamoDB for state locking.
        Ensure best practices for secure storage and state integrity are followed.
        """,
        "outputs": f"""
        Create a Terraform `outputs.tf` file for {service} on {cloud_provider}.
        Define meaningful output variables such as `public_ip`, `instance_id`, or `service_url` to simplify integrations.
        """,
    }

    if include_modules:
        prompts["modules"] = f"""
        Create a Terraform `module` structure for {service} on {cloud_provider}.
        Include reusable module files such as `main.tf`, `variables.tf`, and `outputs.tf`.
        Follow best practices for scalability and maintainability.
        """

    if include_rego:
        prompts["rego_policies"] = f"""
        Create OPA (Open Policy Agent) `rego` policies for {service} on {cloud_provider}.
        Ensure the policies enforce best practices for security, data protection, and resource usage.
        Include sample rules for IAM roles, resource tagging, and encryption enforcement.
        """

    prompts["instructions"] = f"""
    Provide clear instructions for deploying the generated Terraform files.
    Include steps for `terraform init`, `terraform plan`, and `terraform apply`.
    Add best practices for securing state files and backend setup.
    """

    files = {}
    for file_name, prompt in prompts.items():
        files[file_name] = safe_invoke(prompt)

    return files

# Display code and download option
def display_code_with_download(files):
    for file_name, code in files.items():
        if code:
            file_extension = ".tf" if file_name != "instructions" else ".md"
            st.subheader(f"📄 {file_name}.tf")
            st.code(code, language="hcl" if file_extension == ".tf" else "markdown", line_numbers=True)
            file_bytes = BytesIO(code.encode('utf-8'))
            st.download_button(label=f"📥 Download {file_name}{file_extension}", data=file_bytes, file_name=f"{file_name}{file_extension}", mime="text/plain")

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🚀 AI-Powered Terraform Code Generator")

# Sidebar configuration
st.sidebar.header("🔧 Configuration")
cloud_provider = st.sidebar.selectbox("Choose Cloud Provider", ["AWS", "Azure", "GCP"])
service_options = default_services[cloud_provider] + st.session_state.custom_services[cloud_provider]
service = st.sidebar.selectbox("Choose Service", service_options)

include_modules = st.sidebar.checkbox("Include Terraform Modules")
include_rego = st.sidebar.checkbox("Include OPA Rego Policies")

# Add Custom Service
st.sidebar.subheader("➕ Add Custom Service")
custom_service = st.sidebar.text_input("Enter Custom Service Name")
if st.sidebar.button("Add Service"):
    if custom_service.strip():
        st.session_state.custom_services[cloud_provider].append(custom_service.strip())
        st.success(f"✅ {custom_service} added successfully to {cloud_provider} services!")

# Generate configuration
if st.sidebar.button("Generate Configuration"):
    if not cloud_provider or not service:
        st.warning("⚠️ Please select a Cloud Provider and Service before generating the configuration.")
    else:
        st.session_state.refinement_iteration = 0
        generated_files = generate_code(cloud_provider, service, include_modules, include_rego)
        if generated_files:
            st.session_state.generated_files = generated_files
            st.success(f"✅ Terraform Configuration generated successfully!")
            display_code_with_download(generated_files)
