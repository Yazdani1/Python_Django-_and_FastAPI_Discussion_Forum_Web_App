import { type FC } from 'react';
import { Box, IconButton, Tooltip, Typography } from '@mui/material';
import { ThumbUp } from '@mui/icons-material';

interface IVoteButtonsProps {
  voteCount: number;
  isLiked?: boolean;
  onToggle: () => void;
  isLoading?: boolean;
  disabled?: boolean;
}

export const VoteButtons: FC<IVoteButtonsProps> = ({
  voteCount,
  isLiked = false,
  onToggle,
  isLoading = false,
  disabled = false,
}) => {
  const tip = disabled ? 'Log in to like' : isLiked ? 'Remove like' : 'Like';

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
      <Tooltip title={tip}>
        <span>
          <IconButton
            size="small"
            onClick={onToggle}
            disabled={disabled || isLoading}
            color={isLiked ? 'primary' : 'default'}
          >
            <ThumbUp fontSize="small" />
          </IconButton>
        </span>
      </Tooltip>
      <Typography
        variant="body2"
        fontWeight={600}
        sx={{ minWidth: 20, color: isLiked ? 'primary.main' : 'text.secondary' }}
      >
        {voteCount}
      </Typography>
    </Box>
  );
};
