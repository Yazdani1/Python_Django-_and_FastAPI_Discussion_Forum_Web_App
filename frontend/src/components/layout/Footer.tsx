import { Box, Container, Typography } from '@mui/material';

export const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <Box
      component="footer"
      sx={{ py: 3, mt: 'auto', borderTop: 1, borderColor: 'divider', bgcolor: 'background.paper' }}
    >
      <Container maxWidth="lg">
        <Typography variant="body2" color="text.secondary" align="center">
          © {year} Discussion Forum. All rights reserved.
        </Typography>
      </Container>
    </Box>
  );
};
