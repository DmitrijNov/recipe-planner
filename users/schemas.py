from pydantic import BaseModel, Field, model_validator


class RegisterUserRequest(BaseModel):
    username: str = Field(..., examples=["johndoe"])
    email: str = Field(..., examples=["johndoe@example.com"])
    password: str = Field(..., examples=["strongpassword123"])
    confirm_password: str = Field(..., examples=["strongpassword123"])

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self