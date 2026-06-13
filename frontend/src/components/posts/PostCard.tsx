import { type FC } from 'react';
import { useNavigate } from 'react-router-dom';
import {
	Avatar,
	Box,
	Card,
	CardActionArea,
	CardContent,
	Chip,
	Typography,
} from '@mui/material';
import { AccessTime, Person } from '@mui/icons-material';
import { ROUTES } from '@/router/routes';
import type { IPostListItem } from '@/types/post.types';

interface IPostCardProps {
	post: IPostListItem;
}

export const PostCard: FC<IPostCardProps> = ({ post }) => {
	const navigate = useNavigate();

	const formattedDate = new Date(post.created_at).toLocaleDateString('en-US', {
		year: 'numeric',
		month: 'short',
		day: 'numeric',
	});

	return (
		<Card elevation={1} sx={{ mb: 2, '&:hover': { elevation: 3 } }}>
			<CardActionArea onClick={() => navigate(ROUTES.POST_DETAIL(post.id))}>
				<CardContent>
					<Typography variant='h6' fontWeight={600} gutterBottom>
						{post.title}
					</Typography>

					<Typography variant='body2' color='text.secondary' sx={{ mb: 2 }}>
						{post.preview}
						{post.preview.length >= 200 && '…'}
					</Typography>

					<Box
						sx={{
							display: 'flex',
							alignItems: 'center',
							gap: 2,
							flexWrap: 'wrap',
						}}
					>
						<Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
							<Avatar
								src={post.author.avatar_url ?? undefined}
								sx={{
									width: 22,
									height: 22,
									bgcolor: 'secondary.main',
									fontSize: 11,
								}}
							>
								{post.author.username[0].toUpperCase()}
							</Avatar>
							<Typography variant='caption' color='text.secondary'>
								{post.author.username}
							</Typography>
						</Box>

						<Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
							<AccessTime sx={{ fontSize: 14, color: 'text.disabled' }} />
							<Typography variant='caption' color='text.disabled'>
								{formattedDate}
							</Typography>
						</Box>
					</Box>
				</CardContent>
			</CardActionArea>
		</Card>
	);
};
