import api from './api';
import { LoginRequest, RegisterRequest, AuthResponse, User } from './types';

export const authService = {
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await api.post('/auth/login', credentials);
    const { access_token } = response.data;
    
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', access_token);
    }
    
    return { ...response.data, token: access_token };
  },

  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await api.post('/auth/register', userData);
    const { access_token } = response.data;
    
    if (typeof window !== 'undefined') {
      localStorage.setItem('token', access_token);
    }
    
    return { ...response.data, token: access_token };
  },

  async verify(): Promise<User> {
    const response = await api.get('/auth/verify');
    return response.data.user;
  },

  logout(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
  },

  getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token');
    }
    return null;
  },

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
};