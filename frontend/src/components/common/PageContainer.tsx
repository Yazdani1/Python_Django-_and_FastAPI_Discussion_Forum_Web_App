import { type FC, type ReactNode } from 'react';
import { Box, Container, Typography } from '@mui/material';

interface IPageContainerProps {
  children: ReactNode;
  title?: string;
  maxWidth?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
}

export const PageContainer: FC<IPageContainerProps> = ({ children, title, maxWidth = 'lg' }) => {
  return (
    <Container maxWidth={maxWidth}>
      <Box sx={{ py: 4 }}>
        {title && (
          <Typography variant="h4" component="h1" fontWeight={700} sx={{ mb: 3 }}>
            {title}
          </Typography>
        )}
        {children}
      </Box>
    </Container>
  );
};
