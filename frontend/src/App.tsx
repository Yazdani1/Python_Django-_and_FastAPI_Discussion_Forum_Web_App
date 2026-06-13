import { RouterProvider } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { router } from '@/router';
import { QueryProvider } from '@/store/QueryProvider';
import { NotificationProvider } from '@/store/NotificationProvider';
import { AuthProvider } from '@/store/AuthContext';
import { theme } from '@/theme';

export const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <QueryProvider>
        <NotificationProvider>
          <AuthProvider>
            <RouterProvider router={router} />
          </AuthProvider>
        </NotificationProvider>
      </QueryProvider>
    </ThemeProvider>
  );
};
