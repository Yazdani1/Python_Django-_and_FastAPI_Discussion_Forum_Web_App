import { createContext, type FC, type ReactNode, useCallback, useContext, useEffect, useState } from 'react';
import { authService } from '@/services/authService';
import type { IAuthUser, ILoginRequest, IRegisterRequest } from '@/types/auth.types';

interface IAuthContextValue {
  user: IAuthUser | null;
  isLoading: boolean;
  login: (data: ILoginRequest) => Promise<void>;
  register: (data: IRegisterRequest) => Promise<void>;
  logout: () => Promise<void>;
  setUser: (user: IAuthUser | null) => void;
}

const AuthContext = createContext<IAuthContextValue | null>(null);

interface IAuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: FC<IAuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<IAuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    authService
      .getMe()
      .then((res) => {
        if (res.data) setUser(res.data);
      })
      .catch(() => {})
      .finally(() => setIsLoading(false));
  }, []);

  const login = useCallback(async (data: ILoginRequest) => {
    const res = await authService.login(data);
    if (res.data) setUser(res.data);
  }, []);

  const register = useCallback(async (data: IRegisterRequest) => {
    await authService.register(data);
  }, []);

  const logout = useCallback(async () => {
    await authService.logout();
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = (): IAuthContextValue => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuthContext must be used within AuthProvider');
  return ctx;
};
