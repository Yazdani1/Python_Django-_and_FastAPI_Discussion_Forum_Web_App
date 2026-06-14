import { useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import {
  AppBar,
  Box,
  Button,
  Collapse,
  Container,
  IconButton,
  InputBase,
  TextField,
  Toolbar,
  Tooltip,
  Typography,
} from '@mui/material';
import { FilterList, Forum, Search } from '@mui/icons-material';
import { ROUTES } from '@/router/routes';
import { useAuth } from '@/hooks/useAuth';
import { AvatarDropdown } from '@/components/user/AvatarDropdown';

const NAV_BG = '#1e1b4b';
const FILTER_BG = '#2d2a5e';
const ACCENT = '#818cf8';

const darkFieldSx = {
  '& .MuiOutlinedInput-root': {
    color: 'white',
    fontSize: 13,
    '& fieldset': { borderColor: 'rgba(255,255,255,0.18)' },
    '&:hover fieldset': { borderColor: 'rgba(255,255,255,0.4)' },
    '&.Mui-focused fieldset': { borderColor: ACCENT },
  },
  '& .MuiInputLabel-root': { color: 'rgba(255,255,255,0.45)', fontSize: 13 },
  '& .MuiInputLabel-root.Mui-focused': { color: ACCENT },
  input: { '&::-webkit-calendar-picker-indicator': { filter: 'invert(1)' } },
};

export const Navbar = () => {
  const appName = import.meta.env.VITE_APP_NAME ?? 'DiscussHub';
  const { user } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  // Initialise from URL params so refreshing / sharing links keeps inputs in sync
  const [search, setSearch] = useState(() => searchParams.get('search') ?? '');
  const [author, setAuthor] = useState(() => searchParams.get('author') ?? '');
  const [dateFrom, setDateFrom] = useState(() => searchParams.get('date_from') ?? '');
  const [dateTo, setDateTo] = useState(() => searchParams.get('date_to') ?? '');
  const [filtersOpen, setFiltersOpen] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const p = new URLSearchParams();
    if (search.trim()) p.set('search', search.trim());
    if (author.trim()) p.set('author', author.trim());
    if (dateFrom) p.set('date_from', dateFrom);
    if (dateTo) p.set('date_to', dateTo);
    const qs = p.toString();
    navigate(qs ? `${ROUTES.HOME}?${qs}` : ROUTES.HOME);
  };

  const handleClear = () => {
    setSearch('');
    setAuthor('');
    setDateFrom('');
    setDateTo('');
    navigate(ROUTES.HOME);
  };

  const hasActiveFilters = author || dateFrom || dateTo;

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{ bgcolor: NAV_BG, borderBottom: '1px solid rgba(255,255,255,0.07)' }}
    >
      <Container maxWidth="lg">
        <Toolbar disableGutters sx={{ gap: 2, minHeight: { xs: 56, sm: 64 } }}>
          {/* Logo */}
          <Box
            component={Link}
            to={ROUTES.HOME}
            sx={{
              textDecoration: 'none',
              color: 'inherit',
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              flexShrink: 0,
            }}
          >
            <Forum sx={{ color: ACCENT, fontSize: 26 }} />
            <Typography
              variant="h6"
              fontWeight={800}
              sx={{ color: 'white', letterSpacing: '-0.3px' }}
            >
              {appName}
            </Typography>
          </Box>

          {/* Search */}
          <Box
            component="form"
            onSubmit={handleSubmit}
            sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', gap: 1, maxWidth: 520 }}
          >
            <Box
              sx={{
                flexGrow: 1,
                display: 'flex',
                alignItems: 'center',
                bgcolor: 'rgba(255,255,255,0.07)',
                borderRadius: 2,
                px: 1.5,
                border: '1px solid rgba(255,255,255,0.1)',
                transition: 'all 0.2s',
                '&:focus-within': {
                  borderColor: ACCENT,
                  bgcolor: 'rgba(255,255,255,0.1)',
                },
              }}
            >
              <Search
                sx={{ color: 'rgba(255,255,255,0.4)', fontSize: 19, mr: 1, flexShrink: 0 }}
              />
              <InputBase
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search discussions…"
                sx={{
                  flexGrow: 1,
                  color: 'white',
                  fontSize: 14,
                  py: 0.75,
                  '& input::placeholder': { color: 'rgba(255,255,255,0.4)' },
                }}
              />
            </Box>

            <Tooltip title={filtersOpen ? 'Hide filters' : 'More filters'}>
              <IconButton
                onClick={() => setFiltersOpen((v) => !v)}
                size="small"
                sx={{
                  color: filtersOpen || hasActiveFilters ? ACCENT : 'rgba(255,255,255,0.55)',
                  bgcolor: filtersOpen ? 'rgba(99,102,241,0.12)' : 'transparent',
                  border: `1px solid ${filtersOpen ? ACCENT : 'rgba(255,255,255,0.12)'}`,
                  borderRadius: 1.5,
                  p: '6px',
                  '&:hover': { bgcolor: 'rgba(99,102,241,0.12)', borderColor: ACCENT },
                }}
              >
                <FilterList fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>

          <Box sx={{ flexGrow: 1 }} />

          {/* Right side */}
          <Box sx={{ display: 'flex', gap: 1, alignItems: 'center', flexShrink: 0 }}>
            {user ? (
              <AvatarDropdown user={user} />
            ) : (
              <>
                <Button
                  size="small"
                  sx={{ color: 'rgba(255,255,255,0.9)', '&:hover': { color: 'white' } }}
                  onClick={() => navigate(ROUTES.LOGIN)}
                >
                  Sign In
                </Button>
                <Button
                  size="small"
                  variant="outlined"
                  sx={{
                    color: 'white',
                    borderColor: 'rgba(255,255,255,0.28)',
                    '&:hover': { borderColor: 'white', bgcolor: 'rgba(255,255,255,0.06)' },
                  }}
                  onClick={() => navigate(ROUTES.REGISTER)}
                >
                  Register
                </Button>
              </>
            )}
          </Box>
        </Toolbar>
      </Container>

      {/* Filter row */}
      <Collapse in={filtersOpen}>
        <Box
          sx={{ bgcolor: FILTER_BG, borderTop: '1px solid rgba(255,255,255,0.06)' }}
        >
          <Container maxWidth="lg">
            <Box
              component="form"
              onSubmit={handleSubmit}
              sx={{ py: 1.5, display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}
            >
              <TextField
                size="small"
                label="Author"
                value={author}
                onChange={(e) => setAuthor(e.target.value)}
                sx={{ width: 150, ...darkFieldSx }}
              />
              <TextField
                size="small"
                type="date"
                label="From date"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                InputLabelProps={{ shrink: true }}
                sx={{ width: 155, ...darkFieldSx }}
              />
              <TextField
                size="small"
                type="date"
                label="To date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                InputLabelProps={{ shrink: true }}
                sx={{ width: 155, ...darkFieldSx }}
              />
              <Button
                type="submit"
                size="small"
                sx={{ bgcolor: ACCENT, color: 'white', '&:hover': { bgcolor: '#4f46e5' }, px: 2.5 }}
              >
                Apply
              </Button>
              <Button
                size="small"
                onClick={handleClear}
                sx={{ color: 'rgba(255,255,255,0.55)', '&:hover': { color: 'white' } }}
              >
                Clear
              </Button>
            </Box>
          </Container>
        </Box>
      </Collapse>
    </AppBar>
  );
};
