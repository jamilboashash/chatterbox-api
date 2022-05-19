
variable "github_user" {
  type = string
  description = "The GitHub username to use for the container."
  default = "jamilboashash"
}

variable "github_pat" {
  type = string
  description = "The GitHub PAT to use for the container."
  default = "echo $GH_PAT"
}

variable "storage_size" {
  type = number
  description = "The size of the storage to use for the container."
  default = 8
}
