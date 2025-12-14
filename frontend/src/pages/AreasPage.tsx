import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TextField,
  InputAdornment,
  IconButton,
  Chip,
  CircularProgress,
  Alert,
  TableSortLabel,
  Tabs,
  Tab,
} from '@mui/material';
import {
  Search as SearchIcon,
  Clear as ClearIcon,
  Business as BusinessIcon,
  ViewList as ViewListIcon,
  AccountTree as AccountTreeIcon,
} from '@mui/icons-material';
import TabNavigation from '../components/TabNavigation';
import AreaMetricsCards from '../components/AreaMetricsCards';
import AreaHierarchyTree from '../components/AreaHierarchyTree';
import { useAreas, useAreaEmployeeCount, useFirstEmpresa } from '../hooks/useAreas';

type OrderBy = 'area' | 'hierarquia' | 'funcionarios';
type OrderDir = 'asc' | 'desc';

type ViewMode = 'table' | 'tree';

const AreasPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [orderBy, setOrderBy] = useState<OrderBy>('area');
  const [orderDir, setOrderDir] = useState<OrderDir>('asc');
  const [viewMode, setViewMode] = useState<ViewMode>('table');

  const { data: empresaId } = useFirstEmpresa();
  const { data: areas, isLoading: areasLoading, error: areasError } = useAreas(empresaId);
  const { data: contagem, isLoading: contagemLoading } = useAreaEmployeeCount(empresaId);

  const isLoading = areasLoading || contagemLoading;

  // Criar mapa de contagem
  const contagemMap = new Map<string, number>();
  contagem?.forEach((item) => {
    contagemMap.set(item.area_id, item.total_funcionarios);
  });

  // Filtrar áreas por busca
  const filteredAreas = areas?.filter((area) => {
    if (!searchTerm) return true;
    const search = searchTerm.toLowerCase();
    return (
      area.area.toLowerCase().includes(search) ||
      area.diretoria.toLowerCase().includes(search) ||
      area.gerencia.toLowerCase().includes(search) ||
      area.coordenacao.toLowerCase().includes(search)
    );
  });

  // Ordenar áreas
  const sortedAreas = filteredAreas?.sort((a, b) => {
    let comparison = 0;

    switch (orderBy) {
      case 'area':
        comparison = a.area.localeCompare(b.area);
        break;
      case 'hierarquia':
        comparison = `${a.diretoria}/${a.gerencia}/${a.coordenacao}`.localeCompare(
          `${b.diretoria}/${b.gerencia}/${b.coordenacao}`
        );
        break;
      case 'funcionarios':
        const countA = contagemMap.get(a.area_id) || 0;
        const countB = contagemMap.get(b.area_id) || 0;
        comparison = countA - countB;
        break;
    }

    return orderDir === 'asc' ? comparison : -comparison;
  });

  const handleSort = (column: OrderBy) => {
    if (orderBy === column) {
      setOrderDir(orderDir === 'asc' ? 'desc' : 'asc');
    } else {
      setOrderBy(column);
      setOrderDir('asc');
    }
  };

  const handleClearSearch = () => {
    setSearchTerm('');
  };

  const handleAreaClick = (areaId: string) => {
    navigate(`/areas/${areaId}`);
  };

  if (areasError) {
    return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <TabNavigation />
        <Alert severity="error" sx={{ mt: 3 }}>
          Erro ao carregar áreas. Verifique se o backend está rodando.
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <TabNavigation />

      <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', gap: 2 }}>
        <BusinessIcon sx={{ fontSize: 48, color: 'primary.main' }} />
        <Box>
          <Typography variant="h3" component="h1" sx={{ fontWeight: 'bold' }}>
            Áreas Organizacionais
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Estrutura hierárquica e métricas por área
          </Typography>
        </Box>
      </Box>

      <Box sx={{ mb: 4 }}>
        <AreaMetricsCards empresaId={empresaId} />
      </Box>

      <Card elevation={3}>
        <CardContent>
          <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
              {viewMode === 'table' ? 'Lista de Áreas' : 'Estrutura Hierárquica'}
            </Typography>

            <Tabs value={viewMode} onChange={(_: React.SyntheticEvent, value: ViewMode) => setViewMode(value)}>
              <Tab
                icon={<ViewListIcon />}
                iconPosition="start"
                label="Lista"
                value="table"
                sx={{ textTransform: 'none' }}
              />
              <Tab
                icon={<AccountTreeIcon />}
                iconPosition="start"
                label="Árvore"
                value="tree"
                sx={{ textTransform: 'none' }}
              />
            </Tabs>
          </Box>

          {viewMode === 'table' ? (
            <>
              <Box sx={{ mb: 3 }}>
                <TextField
                  fullWidth
                  placeholder="Buscar por nome da área, diretoria, gerência ou coordenação..."
                  value={searchTerm}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchTerm(e.target.value)}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon />
                      </InputAdornment>
                    ),
                    endAdornment: searchTerm && (
                      <InputAdornment position="end">
                        <IconButton size="small" onClick={handleClearSearch}>
                          <ClearIcon />
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
              </Box>

              {isLoading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
                  <CircularProgress />
                </Box>
              ) : (
                <>
                  <TableContainer component={Paper} variant="outlined">
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>
                            <TableSortLabel
                              active={orderBy === 'area'}
                              direction={orderBy === 'area' ? orderDir : 'asc'}
                              onClick={() => handleSort('area')}
                            >
                              Área
                            </TableSortLabel>
                          </TableCell>
                          <TableCell>
                            <TableSortLabel
                              active={orderBy === 'hierarquia'}
                              direction={orderBy === 'hierarquia' ? orderDir : 'asc'}
                              onClick={() => handleSort('hierarquia')}
                            >
                              Hierarquia
                            </TableSortLabel>
                          </TableCell>
                          <TableCell align="center">
                            <TableSortLabel
                              active={orderBy === 'funcionarios'}
                              direction={orderBy === 'funcionarios' ? orderDir : 'asc'}
                              onClick={() => handleSort('funcionarios')}
                            >
                              Funcionários
                            </TableSortLabel>
                          </TableCell>
                          <TableCell align="center">Ações</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {sortedAreas && sortedAreas.length > 0 ? (
                          sortedAreas.map((area) => (
                            <TableRow
                              key={area.area_id}
                              hover
                              sx={{ cursor: 'pointer' }}
                              onClick={() => handleAreaClick(area.area_id)}
                            >
                              <TableCell>
                                <Typography variant="body1" sx={{ fontWeight: 600 }}>
                                  {area.area}
                                </Typography>
                              </TableCell>
                              <TableCell>
                                <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                                  <Chip label={area.diretoria} size="small" color="primary" variant="outlined" />
                                  <Typography variant="body2" sx={{ mx: 0.5 }}>
                                    →
                                  </Typography>
                                  <Chip label={area.gerencia} size="small" color="success" variant="outlined" />
                                  <Typography variant="body2" sx={{ mx: 0.5 }}>
                                    →
                                  </Typography>
                                  <Chip label={area.coordenacao} size="small" color="warning" variant="outlined" />
                                </Box>
                              </TableCell>
                              <TableCell align="center">
                                <Chip
                                  label={contagemMap.get(area.area_id) || 0}
                                  color="default"
                                  sx={{ fontWeight: 600 }}
                                />
                              </TableCell>
                              <TableCell align="center">
                                <Chip
                                  label="Ver Detalhes"
                                  color="primary"
                                  size="small"
                                  onClick={(e: React.MouseEvent) => {
                                    e.stopPropagation();
                                    handleAreaClick(area.area_id);
                                  }}
                                />
                              </TableCell>
                            </TableRow>
                          ))
                        ) : (
                          <TableRow>
                            <TableCell colSpan={4} align="center" sx={{ py: 8 }}>
                              <SearchIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                              <Typography variant="h6" color="text.secondary">
                                {searchTerm
                                  ? `Nenhuma área encontrada para "${searchTerm}"`
                                  : 'Nenhuma área disponível'}
                              </Typography>
                            </TableCell>
                          </TableRow>
                        )}
                      </TableBody>
                    </Table>
                  </TableContainer>

                  {sortedAreas && sortedAreas.length > 0 && (
                    <Box
                      sx={{
                        mt: 2,
                        p: 2,
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        borderTop: 1,
                        borderColor: 'divider',
                        bgcolor: 'grey.50',
                      }}
                    >
                      <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                        Mostrando {sortedAreas.length} de {areas?.length || 0} áreas
                      </Typography>
                      {searchTerm && (
                        <Chip
                          label={`Buscando: "${searchTerm}"`}
                          onDelete={handleClearSearch}
                          color="primary"
                          size="small"
                        />
                      )}
                    </Box>
                  )}
                </>
              )}
            </>
          ) : (
            <AreaHierarchyTree empresaId={empresaId} onAreaClick={handleAreaClick} />
          )}
        </CardContent>
      </Card>
    </Container>
  );
};

export default AreasPage;
