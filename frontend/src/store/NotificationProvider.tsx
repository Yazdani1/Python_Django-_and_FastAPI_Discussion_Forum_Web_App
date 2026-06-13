import { type FC, type ReactNode } from 'react';
import { SnackbarProvider } from 'notistack';

interface INotificationProviderProps {
  children: ReactNode;
}

export const NotificationProvider: FC<INotificationProviderProps> = ({ children }) => {
  return (
    <SnackbarProvider
      maxSnack={4}
      anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      autoHideDuration={4000}
    >
      {children}
    </SnackbarProvider>
  );
};
