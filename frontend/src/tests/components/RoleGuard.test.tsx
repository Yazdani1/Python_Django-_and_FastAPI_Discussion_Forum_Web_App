import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { RoleGuard } from '@/components/guards/RoleGuard';
import type { IAuthUser } from '@/types/auth.types';

const adminUser: IAuthUser = { id: '1', email: 'a@a.com', username: 'admin', role: 'admin', avatar_url: null };
const regularUser: IAuthUser = { id: '2', email: 'b@b.com', username: 'user', role: 'user', avatar_url: null };

vi.mock('@/hooks/useAuth', () => ({
  useAuth: vi.fn(),
}));

import { useAuth } from '@/hooks/useAuth';
const mockUseAuth = vi.mocked(useAuth);

function renderGuard(user: IAuthUser | null, requiredRole: IAuthUser['role']) {
  mockUseAuth.mockReturnValue({
    user,
    isLoading: false,
    login: vi.fn(),
    register: vi.fn(),
    logout: vi.fn(),
    setUser: vi.fn(),
  });

  return render(
    <MemoryRouter>
      <RoleGuard requiredRole={requiredRole} fallback={<div>Access denied</div>}>
        <div>Protected content</div>
      </RoleGuard>
    </MemoryRouter>,
  );
}

describe('RoleGuard', () => {
  it('renders children when user role meets requirement', () => {
    renderGuard(adminUser, 'moderator');
    expect(screen.getByText('Protected content')).toBeInTheDocument();
  });

  it('renders fallback when user role is insufficient', () => {
    renderGuard(regularUser, 'admin');
    expect(screen.getByText('Access denied')).toBeInTheDocument();
    expect(screen.queryByText('Protected content')).not.toBeInTheDocument();
  });

  it('renders fallback when user is null', () => {
    renderGuard(null, 'user');
    expect(screen.getByText('Access denied')).toBeInTheDocument();
  });

  it('allows exact role match', () => {
    renderGuard(regularUser, 'user');
    expect(screen.getByText('Protected content')).toBeInTheDocument();
  });
});
