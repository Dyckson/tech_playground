import { Box, Tabs, Tab } from '@mui/material';
import { Dashboard as DashboardIcon, Business as BusinessIcon, Group as GroupIcon } from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const TabNavigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleChange = (_event: React.SyntheticEvent, newValue: string) => {
    navigate(newValue);
  };

  const getCurrentValue = () => {
    if (location.pathname === '/') return '/';
    if (location.pathname.startsWith('/areas')) return '/areas';
    if (location.pathname.startsWith('/employees')) return '/employees';
    return '/';
  };

  return (
    <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
      <Tabs
        value={getCurrentValue()}
        onChange={handleChange}
        aria-label="navegação principal"
        variant="fullWidth"
        sx={{
          '& .MuiTab-root': {
            minHeight: 64,
            textTransform: 'none',
            fontSize: '1rem',
            fontWeight: 500,
          },
        }}
      >
        <Tab
          icon={<DashboardIcon />}
          iconPosition="start"
          label="Dashboard"
          value="/"
        />
        <Tab
          icon={<BusinessIcon />}
          iconPosition="start"
          label="Áreas"
          value="/areas"
          disabled
        />
        <Tab
          icon={<GroupIcon />}
          iconPosition="start"
          label="Funcionários"
          value="/employees"
        />
      </Tabs>
    </Box>
  );
};

TabNavigation.displayName = 'TabNavigation';

export default TabNavigation;
