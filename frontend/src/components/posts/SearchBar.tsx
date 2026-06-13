import { type FC, useState } from 'react';
import { Box, Button, TextField } from '@mui/material';
import { Search } from '@mui/icons-material';
import type { IPostSearchParams } from '@/types/post.types';

interface ISearchBarProps {
  onSearch: (params: IPostSearchParams) => void;
  initialParams?: IPostSearchParams;
}

export const SearchBar: FC<ISearchBarProps> = ({ onSearch, initialParams = {} }) => {
  const [search, setSearch] = useState(initialParams.search ?? '');
  const [dateFrom, setDateFrom] = useState(initialParams.date_from ?? '');
  const [dateTo, setDateTo] = useState(initialParams.date_to ?? '');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch({
      search: search || undefined,
      date_from: dateFrom || undefined,
      date_to: dateTo || undefined,
      page: 1,
    });
  };

  const handleClear = () => {
    setSearch('');
    setDateFrom('');
    setDateTo('');
    onSearch({ page: 1 });
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center', mb: 3 }}
    >
      <TextField
        label="Search posts"
        size="small"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        sx={{ flexGrow: 1, minWidth: 200 }}
      />

      <TextField
        label="From date"
        type="date"
        size="small"
        value={dateFrom}
        onChange={(e) => setDateFrom(e.target.value)}
        InputLabelProps={{ shrink: true }}
        sx={{ width: 160 }}
      />

      <TextField
        label="To date"
        type="date"
        size="small"
        value={dateTo}
        onChange={(e) => setDateTo(e.target.value)}
        InputLabelProps={{ shrink: true }}
        sx={{ width: 160 }}
      />

      <Button type="submit" variant="contained" startIcon={<Search />}>
        Search
      </Button>

      <Button type="button" variant="outlined" onClick={handleClear}>
        Clear
      </Button>
    </Box>
  );
};
