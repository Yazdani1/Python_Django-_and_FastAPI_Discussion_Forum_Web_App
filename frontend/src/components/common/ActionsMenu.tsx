import { useState, type FC, type ReactNode } from 'react';
import { IconButton, ListItemIcon, Menu, MenuItem, Tooltip, Typography } from '@mui/material';
import { MoreVert } from '@mui/icons-material';

export interface IActionsMenuItem {
  label: string;
  icon?: ReactNode;
  onClick: () => void;
  color?: 'error';
  disabled?: boolean;
}

interface IActionsMenuProps {
  items: IActionsMenuItem[];
}

export const ActionsMenu: FC<IActionsMenuProps> = ({ items }) => {
  const [anchor, setAnchor] = useState<null | HTMLElement>(null);
  const open = Boolean(anchor);

  const handleOpen = (e: React.MouseEvent<HTMLElement>) => {
    e.stopPropagation();
    setAnchor(e.currentTarget);
  };

  const handleClose = (e: React.MouseEvent) => {
    e.stopPropagation();
    setAnchor(null);
  };

  const handleItemClick = (e: React.MouseEvent, fn: () => void) => {
    e.stopPropagation();
    setAnchor(null);
    fn();
  };

  return (
    <>
      <Tooltip title="More options">
        <IconButton size="small" onClick={handleOpen} sx={{ color: 'text.disabled' }}>
          <MoreVert fontSize="small" />
        </IconButton>
      </Tooltip>

      <Menu
        anchorEl={anchor}
        open={open}
        onClose={handleClose}
        onClick={(e) => e.stopPropagation()}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        slotProps={{ paper: { elevation: 3, sx: { minWidth: 130 } } }}
      >
        {items.map((item) => (
          <MenuItem
            key={item.label}
            onClick={(e) => handleItemClick(e, item.onClick)}
            disabled={item.disabled}
            sx={{ gap: 1, color: item.color === 'error' ? 'error.main' : 'text.primary' }}
          >
            {item.icon && (
              <ListItemIcon sx={{ color: 'inherit', minWidth: 'auto' }}>
                {item.icon}
              </ListItemIcon>
            )}
            <Typography variant="body2">{item.label}</Typography>
          </MenuItem>
        ))}
      </Menu>
    </>
  );
};
