import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { PageContainer } from '@/components/common/PageContainer';

describe('PageContainer', () => {
  it('renders children', () => {
    render(<PageContainer><p>Child content</p></PageContainer>);
    expect(screen.getByText('Child content')).toBeInTheDocument();
  });

  it('renders title when provided', () => {
    render(<PageContainer title="My Title"><p>Content</p></PageContainer>);
    expect(screen.getByRole('heading', { name: 'My Title' })).toBeInTheDocument();
  });

  it('does not render heading when title is omitted', () => {
    render(<PageContainer><p>No title</p></PageContainer>);
    expect(screen.queryByRole('heading')).not.toBeInTheDocument();
  });
});
