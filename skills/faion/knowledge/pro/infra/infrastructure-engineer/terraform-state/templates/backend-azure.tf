terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "COMPANYtfstate"
    container_name       = "tfstate"
    key                  = "ENV/COMPONENT/terraform.tfstate"
    use_azuread_auth     = true
  }
}
