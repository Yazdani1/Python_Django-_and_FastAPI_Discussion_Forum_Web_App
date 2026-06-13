import { type FC, type ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import type { TUserRole } from '@/types/auth.types';
import { ROUTES } from '@/router/routes';
import { useAuth } from '@/hooks/useAuth';

const ROLE_LEVELS: Record<TUserRole, number> = {
  guest: 0,
  user: 1,
  moderator: 2,
  admin: 3,
};

interface IRoleGuardProps {
  children: ReactNode;
  requiredRole: TUserRole;
  redirectTo?: string;
  fallback?: ReactNode;
}

export const RoleGuard: FC<IRoleGuardProps> = ({
  children,
  requiredRole,
  redirectTo = ROUTES.HOME,
  fallback,
}) => {
  const { user } = useAuth();

  if (!user) {
    return fallback ? <>{fallback}</> : <Navigate to={redirectTo} replace />;
  }

  const userLevel = ROLE_LEVELS[user.role];
  const requiredLevel = ROLE_LEVELS[requiredRole];

  if (userLevel < requiredLevel) {
    return fallback ? <>{fallback}</> : <Navigate to={redirectTo} replace />;
  }

  return <>{children}</>;
};
