import { Box, Button, Typography } from '@mui/material';
import { Link } from 'react-router-dom';
import { ROUTES } from '@/router/routes';

const NotFoundPage = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        gap: 2,
      }}
    >
      <Typography variant="h1" fontWeight={700} color="text.secondary">
        404
      </Typography>
      <Typography variant="h5" color="text.secondary">
        Page not found
      </Typography>
      <Button component={Link} to={ROUTES.HOME} variant="contained" size="large">
        Go Home
      </Button>
    </Box>
  );
};

export default NotFoundPage;
