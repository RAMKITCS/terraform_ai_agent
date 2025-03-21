# 🚀 AI-Powered Terraform Code Generator

This AI-powered Terraform Code Generator automates the creation of Infrastructure as Code (IaC) configurations for AWS, Azure, and GCP services. It leverages **OpenAI GPT-4o** to dynamically generate secure, scalable, and modular Terraform code, including optional Terraform modules and OPA Rego policies for security compliance.

---

## 📋 Features
✅ **Generates `main.tf`, `variables.tf`, `provider.tf`, `backend.tf`, and `outputs.tf`** files following best practices.  
✅ **Option to Include Modular Terraform Code** for scalability.  
✅ **Option to Generate OPA Rego Policies** for enforcing security and compliance.  
✅ **Automatic Provider Separation** with a dedicated `provider.tf`.  
✅ **Refinement Capabilities** — Users can provide feedback to refine configurations iteratively.  
✅ **Downloadable Files** for direct integration into your project.  

---

## 📦 Prerequisites
- Python 3.10 or higher
- An **OpenAI API Key** (set in `.env` file)
- Required Python Libraries:

```bash
pip install streamlit langchain_openai python-dotenv
```

---

## ⚙️ Setup Instructions

1. **Clone the Repository**
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Set the OpenAI API Key**
Create a `.env` file in the root directory and add the following:
```
OPENAI_API_KEY=<your_openai_api_key>
```

4. **Run the Streamlit Application**
```bash
streamlit run <your_script_name>.py
```

---

## 🖥️ How to Use

1. **Select Cloud Provider:** Choose between `AWS`, `Azure`, or `GCP`.
2. **Select Service:** Choose from predefined services or add your own using the **Add Custom Service** option.
3. **Select Additional Options:**
   - ✅ **Include Terraform Modules** for modularization.  
   - ✅ **Include OPA Rego Policies** for security best practices.  
4. **Generate Configuration:** Click **"Generate Configuration"** to create Terraform files.
5. **Download the Files:** Each generated file will include a **Download** button.
6. **Refine Configuration:** Enter improvement suggestions (e.g., "Add CloudWatch logs", "Enforce resource tagging") in the **Refinement Section** for customized updates.

---

## 🛠️ Deployment Instructions
After generating your Terraform configuration:

1. **Initialize Terraform**
```bash
terraform init
```

2. **Plan Deployment**
```bash
terraform plan
```

3. **Apply Changes**
```bash
terraform apply
```

---

## 🔎 Example Feedback for Refinement
- _"Add CloudWatch logs for instance monitoring."_  
- _"Add lifecycle rules to prevent accidental deletion."_  
- _"Improve IAM policy with least privilege access."_  

---

## 🚧 Future Enhancements
✅ Dynamic backend configuration for various cloud providers  
✅ Enhanced CloudWatch integration for monitoring  
✅ Improved error handling for seamless deployment experience  



