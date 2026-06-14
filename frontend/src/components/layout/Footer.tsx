import { Box, Container, Divider, Grid, Link as MuiLink, Typography } from '@mui/material';
import { Forum } from '@mui/icons-material';
import { Link } from 'react-router-dom';
import { ROUTES } from '@/router/routes';

const FOOTER_BG = '#0f172a';
const MUTED = 'rgba(255,255,255,0.45)';
const LINK_COLOR = 'rgba(255,255,255,0.7)';

interface IFooterLinkProps {
  to: string;
  children: React.ReactNode;
}

const FooterLink = ({ to, children }: IFooterLinkProps) => (
  <MuiLink
    component={Link}
    to={to}
    underline="none"
    sx={{
      display: 'block',
      color: LINK_COLOR,
      fontSize: 14,
      mb: 1,
      '&:hover': { color: 'white' },
      transition: 'color 0.15s',
    }}
  >
    {children}
  </MuiLink>
);

const SectionTitle = ({ children }: { children: React.ReactNode }) => (
  <Typography
    variant="caption"
    sx={{
      color: MUTED,
      fontWeight: 700,
      letterSpacing: '0.08em',
      textTransform: 'uppercase',
      display: 'block',
      mb: 2,
    }}
  >
    {children}
  </Typography>
);

export const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <Box
      component="footer"
      sx={{ bgcolor: FOOTER_BG, color: 'white', mt: 'auto', pt: 6, pb: 3 }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={5}>
          {/* Branding */}
          <Grid item xs={12} sm={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
              <Forum sx={{ color: '#6366f1', fontSize: 24 }} />
              <Typography variant="h6" fontWeight={800} sx={{ letterSpacing: '-0.3px' }}>
                DiscussHub
              </Typography>
            </Box>
            <Typography variant="body2" sx={{ color: MUTED, lineHeight: 1.7, maxWidth: 260 }}>
              A place where ideas meet open discussion. Ask questions, share knowledge, and connect with a growing community.
            </Typography>
            <Typography variant="caption" sx={{ color: MUTED, mt: 2, display: 'block' }}>
              Built with FastAPI &amp; React
            </Typography>
          </Grid>

          {/* Navigation */}
          <Grid item xs={6} sm={2}>
            <SectionTitle>Navigate</SectionTitle>
            <FooterLink to={ROUTES.HOME}>Home</FooterLink>
            <FooterLink to={ROUTES.LOGIN}>Sign In</FooterLink>
            <FooterLink to={ROUTES.REGISTER}>Register</FooterLink>
            <FooterLink to={ROUTES.CREATE_POST}>New Post</FooterLink>
          </Grid>

          {/* Community */}
          <Grid item xs={6} sm={2}>
            <SectionTitle>Community</SectionTitle>
            <MuiLink
              href="#"
              underline="none"
              sx={{ display: 'block', color: LINK_COLOR, fontSize: 14, mb: 1, '&:hover': { color: 'white' } }}
            >
              GitHub
            </MuiLink>
            <MuiLink
              href="#"
              underline="none"
              sx={{ display: 'block', color: LINK_COLOR, fontSize: 14, mb: 1, '&:hover': { color: 'white' } }}
            >
              Discord
            </MuiLink>
            <MuiLink
              href="#"
              underline="none"
              sx={{ display: 'block', color: LINK_COLOR, fontSize: 14, mb: 1, '&:hover': { color: 'white' } }}
            >
              Twitter / X
            </MuiLink>
          </Grid>

          {/* Legal */}
          <Grid item xs={6} sm={2}>
            <SectionTitle>Legal</SectionTitle>
            <MuiLink
              href="#"
              underline="none"
              sx={{ display: 'block', color: LINK_COLOR, fontSize: 14, mb: 1, '&:hover': { color: 'white' } }}
            >
              Privacy Policy
            </MuiLink>
            <MuiLink
              href="#"
              underline="none"
              sx={{ display: 'block', color: LINK_COLOR, fontSize: 14, mb: 1, '&:hover': { color: 'white' } }}
            >
              Terms of Use
            </MuiLink>
            <MuiLink
              href="#"
              underline="none"
              sx={{ display: 'block', color: LINK_COLOR, fontSize: 14, mb: 1, '&:hover': { color: 'white' } }}
            >
              Cookie Policy
            </MuiLink>
          </Grid>
        </Grid>

        <Divider sx={{ my: 4, borderColor: 'rgba(255,255,255,0.08)' }} />

        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 1 }}>
          <Typography variant="body2" sx={{ color: MUTED }}>
            © {year} DiscussHub. All rights reserved.
          </Typography>
          <Typography variant="body2" sx={{ color: MUTED }}>
            Made with FastAPI, PostgreSQL, Redis &amp; React
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};
