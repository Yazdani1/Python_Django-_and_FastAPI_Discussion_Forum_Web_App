import { type FC, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Avatar, Box, IconButton, ListItemIcon, Menu, MenuItem, Typography } from '@mui/material';
import { ExitToApp, Person } from '@mui/icons-material';
import { useAuth } from '@/hooks/useAuth';
import { ROUTES } from '@/router/routes';
import type { IAuthUser } from '@/types/auth.types';

interface IAvatarDropdownProps {
  user: IAuthUser;
}

export const AvatarDropdown: FC<IAvatarDropdownProps> = ({ user }) => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const initials = user.username.slice(0, 2).toUpperCase();

  const handleOpen = (e: React.MouseEvent<HTMLElement>) => setAnchorEl(e.currentTarget);
  const handleClose = () => setAnchorEl(null);

  const handleProfile = () => {
    handleClose();
    navigate(ROUTES.PROFILE);
  };

  const handleLogout = async () => {
    handleClose();
    await logout();
    navigate(ROUTES.HOME);
  };

  return (
    <Box>
      <IconButton onClick={handleOpen} sx={{ p: 0 }}>
        <Avatar
          src={user.avatar_url ?? undefined}
          sx={{ bgcolor: 'secondary.main', width: 36, height: 36 }}
        >
          {!user.avatar_url && initials}
        </Avatar>
      </IconButton>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleClose}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <MenuItem disabled>
          <Typography variant="caption" color="text.secondary">
            {user.username}
          </Typography>
        </MenuItem>

        <MenuItem onClick={handleProfile}>
          <ListItemIcon>
            <Person fontSize="small" />
          </ListItemIcon>
          View Profile
        </MenuItem>

        <MenuItem onClick={handleLogout}>
          <ListItemIcon>
            <ExitToApp fontSize="small" />
          </ListItemIcon>
          Logout
        </MenuItem>
      </Menu>
    </Box>
  );
};
