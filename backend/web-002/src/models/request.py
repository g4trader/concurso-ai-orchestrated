"""
Modelos de Request para WEB-002
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class LoginRequest(BaseModel):
    """Request para login"""
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., description="Senha do usuário", min_length=8)
    remember_me: bool = Field(False, description="Lembrar usuário")

class RegisterRequest(BaseModel):
    """Request para registro"""
    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., description="Senha do usuário", min_length=8)
    name: str = Field(..., description="Nome do usuário", min_length=2)
    confirm_password: str = Field(..., description="Confirmação da senha")

class RefreshTokenRequest(BaseModel):
    """Request para refresh token"""
    refresh_token: str = Field(..., description="Token de refresh")

class ForgotPasswordRequest(BaseModel):
    """Request para recuperação de senha"""
    email: EmailStr = Field(..., description="Email do usuário")

class ResetPasswordRequest(BaseModel):
    """Request para reset de senha"""
    token: str = Field(..., description="Token de reset")
    new_password: str = Field(..., description="Nova senha", min_length=8)
    confirm_password: str = Field(..., description="Confirmação da nova senha")

class ChangePasswordRequest(BaseModel):
    """Request para mudança de senha"""
    current_password: str = Field(..., description="Senha atual")
    new_password: str = Field(..., description="Nova senha", min_length=8)
    confirm_password: str = Field(..., description="Confirmação da nova senha")

class UpdateProfileRequest(BaseModel):
    """Request para atualização de perfil"""
    name: Optional[str] = Field(None, description="Nome do usuário", min_length=2)
    avatar: Optional[str] = Field(None, description="URL do avatar")

class HealthCheckRequest(BaseModel):
    """Request para health check"""
    check_components: Optional[bool] = Field(False, description="Verificar componentes")

class MetricsRequest(BaseModel):
    """Request para métricas"""
    time_range: Optional[str] = Field("1h", description="Período das métricas")
