"""
Modelos de Response para WEB-002
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class User(BaseModel):
    """Modelo de usuário"""
    id: str = Field(..., description="ID único do usuário")
    email: str = Field(..., description="Email do usuário")
    name: str = Field(..., description="Nome do usuário")
    avatar: Optional[str] = Field(None, description="URL do avatar")
    created_at: datetime = Field(..., description="Data de criação")
    last_login: Optional[datetime] = Field(None, description="Último login")
    is_active: bool = Field(True, description="Se o usuário está ativo")

class LoginResponse(BaseModel):
    """Response para login"""
    user: User = Field(..., description="Dados do usuário")
    token: str = Field(..., description="Token JWT de acesso")
    refresh_token: str = Field(..., description="Token para refresh")
    expires_in: int = Field(..., description="Tempo de expiração em segundos")
    token_type: str = Field("Bearer", description="Tipo do token")

class LogoutResponse(BaseModel):
    """Response para logout"""
    message: str = Field(..., description="Mensagem de confirmação")
    logged_out_at: datetime = Field(..., description="Horário do logout")

class RefreshTokenResponse(BaseModel):
    """Response para refresh token"""
    token: str = Field(..., description="Novo token JWT")
    refresh_token: str = Field(..., description="Novo token de refresh")
    expires_in: int = Field(..., description="Tempo de expiração em segundos")
    token_type: str = Field("Bearer", description="Tipo do token")

class RegisterResponse(BaseModel):
    """Response para registro"""
    user: User = Field(..., description="Dados do usuário criado")
    message: str = Field(..., description="Mensagem de confirmação")

class ForgotPasswordResponse(BaseModel):
    """Response para recuperação de senha"""
    message: str = Field(..., description="Mensagem de confirmação")
    email_sent: bool = Field(..., description="Se o email foi enviado")

class ResetPasswordResponse(BaseModel):
    """Response para reset de senha"""
    message: str = Field(..., description="Mensagem de confirmação")
    success: bool = Field(..., description="Se o reset foi bem-sucedido")

class ChangePasswordResponse(BaseModel):
    """Response para mudança de senha"""
    message: str = Field(..., description="Mensagem de confirmação")
    success: bool = Field(..., description="Se a mudança foi bem-sucedida")

class UpdateProfileResponse(BaseModel):
    """Response para atualização de perfil"""
    user: User = Field(..., description="Dados atualizados do usuário")
    message: str = Field(..., description="Mensagem de confirmação")

class HealthResponse(BaseModel):
    """Response para health check"""
    status: str = Field(..., description="Status da aplicação")
    details: Dict[str, Any] = Field(..., description="Detalhes do status")

class MetricsResponse(BaseModel):
    """Response para métricas"""
    metrics: Dict[str, Any] = Field(..., description="Métricas do sistema")

class ErrorResponse(BaseModel):
    """Response para erros"""
    error: str = Field(..., description="Descrição do erro")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalhes do erro")
