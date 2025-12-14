import { Card, CardContent, Box, Typography, Chip, Avatar, Grid, Divider } from '@mui/material';
import {
  Person as PersonIcon,
  Work as WorkIcon,
  Business as BusinessIcon,
  LocationOn as LocationIcon,
  CalendarToday as CalendarIcon,
  Groups as GroupsIcon,
} from '@mui/icons-material';

interface EmployeeProfileCardProps {
  employee: {
    nome: string;
    email: string;
    cargo_nome: string;
    area_nome: string;
    localidade_nome: string;
    tempo_empresa_nome: string;
    genero_nome: string;
    geracao_nome: string;
  };
}

const EmployeeProfileCard: React.FC<EmployeeProfileCardProps> = ({ employee }) => {
  const getInitials = (name: string) => {
    const parts = name.split(' ');
    return parts.length >= 2 
      ? `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase()
      : name.substring(0, 2).toUpperCase();
  };

  return (
    <Card elevation={3}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <Avatar
            sx={{
              width: 80,
              height: 80,
              bgcolor: 'primary.main',
              fontSize: '2rem',
              mr: 2,
            }}
          >
            {getInitials(employee.nome)}
          </Avatar>
          <Box>
            <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
              {employee.nome}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ display: 'flex', alignItems: 'center', gap: 0.5, mt: 0.5 }}>
              <PersonIcon fontSize="small" />
              {employee.email}
            </Typography>
          </Box>
        </Box>

        <Divider sx={{ my: 2 }} />

        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1.5 }}>
              <WorkIcon color="action" fontSize="small" />
              <Box>
                <Typography variant="caption" color="text.secondary" display="block">
                  Cargo
                </Typography>
                <Typography variant="body2" sx={{ fontWeight: 500 }}>
                  {employee.cargo_nome}
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1.5 }}>
              <BusinessIcon color="action" fontSize="small" />
              <Box>
                <Typography variant="caption" color="text.secondary" display="block">
                  Área
                </Typography>
                <Typography variant="body2" sx={{ fontWeight: 500 }}>
                  {employee.area_nome}
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1.5 }}>
              <LocationIcon color="action" fontSize="small" />
              <Box>
                <Typography variant="caption" color="text.secondary" display="block">
                  Localidade
                </Typography>
                <Typography variant="body2" sx={{ fontWeight: 500 }}>
                  {employee.localidade_nome}
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1.5 }}>
              <CalendarIcon color="action" fontSize="small" />
              <Box>
                <Typography variant="caption" color="text.secondary" display="block">
                  Tempo de Casa
                </Typography>
                <Typography variant="body2" sx={{ fontWeight: 500 }}>
                  {employee.tempo_empresa_nome}
                </Typography>
              </Box>
            </Box>
          </Grid>
        </Grid>

        <Divider sx={{ my: 2 }} />

        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          <Chip
            icon={<GroupsIcon />}
            label={employee.geracao_nome}
            size="small"
            color="primary"
            variant="outlined"
          />
          <Chip
            label={employee.genero_nome}
            size="small"
            color="secondary"
            variant="outlined"
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default EmployeeProfileCard;
