terraform {
  cloud {
    organization = "ORGANIZATION"

    workspaces {
      name = "ENV-COMPONENT"
    }
  }
}
