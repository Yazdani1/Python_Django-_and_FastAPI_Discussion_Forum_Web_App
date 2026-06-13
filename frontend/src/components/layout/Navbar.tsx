import { AppBar, Box, Button, Container, Toolbar, Typography } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import { ROUTES } from '@/router/routes';
import { useAuth } from '@/hooks/useAuth';
import { AvatarDropdown } from '@/components/user/AvatarDropdown';

export const Navbar = () => {
  const appName = import.meta.env.VITE_APP_NAME ?? 'Discussion Forum';
  const { user } = useAuth();
  const navigate = useNavigate();

  return (
    <AppBar position="sticky" elevation={1}>
      <Container maxWidth="lg">
        <Toolbar disableGutters>
          <Box component={Link} to={ROUTES.HOME} sx={{ textDecoration: 'none', color: 'inherit' }}>
            <Typography variant="h6" fontWeight={700}>
              {appName}
            </Typography>
          </Box>

          <Box sx={{ flexGrow: 1 }} />

          {user ? (
            <AvatarDropdown user={user} />
          ) : (
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button color="inherit" onClick={() => navigate(ROUTES.LOGIN)}>
                Sign In
              </Button>
              <Button
                variant="outlined"
                color="inherit"
                onClick={() => navigate(ROUTES.REGISTER)}
                sx={{ borderColor: 'rgba(255,255,255,0.5)' }}
              >
                Register
              </Button>
            </Box>
          )}
        </Toolbar>
      </Container>
    </AppBar>
  );
};
