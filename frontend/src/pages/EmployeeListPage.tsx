import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  Container,
  Box,
  Typography,
  TextField,
  InputAdornment,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Paper,
  IconButton,
  CircularProgress,
  Alert,
  Chip,
  Button,
  TableSortLabel,
  Tooltip,
} from '@mui/material';
import {
  Search as SearchIcon,
  Visibility as VisibilityIcon,
  Download as DownloadIcon,
} from '@mui/icons-material';
import axios from 'axios';
import TabNavigation from '../components/TabNavigation';
import EmployeeFilterBar, { FilterValues } from '../components/EmployeeFilterBar';

type OrderBy = 'nome' | 'cargo' | 'area' | 'tempo' | 'score';
type OrderDir = 'asc' | 'desc';

const EmployeeListPage = () => {
  const navigate = useNavigate();
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');
  const [orderBy, setOrderBy] = useState<OrderBy>('nome');
  const [orderDir, setOrderDir] = useState<OrderDir>('asc');
  const [filters, setFilters] = useState<FilterValues>({
    cargos: [],
    areas: [],
    temposCasa: [],
    scoreMin: '',
    scoreMax: '',
    enpsStatus: '',
  });

  const { data, isLoading, error } = useQuery({
    queryKey: ['employees', page + 1, rowsPerPage, filters, orderBy, orderDir, searchTerm],
    queryFn: async () => {
      const params: any = {
        page: page + 1,
        page_size: rowsPerPage,
        order_by: orderBy,
        order_dir: orderDir,
      };

      if (filters.cargos.length > 0) params.cargos = filters.cargos;
      if (filters.areas.length > 0) params.areas = filters.areas;
      if (filters.temposCasa.length > 0) params.tempo_casa = filters.temposCasa;
      if (filters.scoreMin) params.score_min = parseFloat(filters.scoreMin);
      if (filters.scoreMax) params.score_max = parseFloat(filters.scoreMax);
      if (filters.enpsStatus) params.enps_status = filters.enpsStatus;

      // Se houver termo de busca, usar endpoint de busca
      const endpoint = searchTerm.trim().length >= 2 
        ? 'http://localhost:9876/api/v1/funcionarios/buscar'
        : 'http://localhost:9876/api/v1/funcionarios';
      
      if (searchTerm.trim().length >= 2) {
        params.termo = searchTerm.trim();
      }

      const { data } = await axios.get(endpoint, { 
        params,
        paramsSerializer: {
          indexes: null, // Envia arrays como param=val1&param=val2
        }
      });
      
      return data;
    },
  });

  const handleChangePage = (_event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
    setPage(0); // Resetar para primeira página ao buscar
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleSort = (column: OrderBy) => {
    if (orderBy === column) {
      setOrderDir(orderDir === 'asc' ? 'desc' : 'asc');
    } else {
      setOrderBy(column);
      setOrderDir('asc');
    }
    setPage(0);
  };

  const handleFilterChange = (newFilters: FilterValues) => {
    setFilters(newFilters);
    setPage(0);
  };

  const handleClearFilters = () => {
    setFilters({
      cargos: [],
      areas: [],
      temposCasa: [],
      scoreMin: '',
      scoreMax: '',
      enpsStatus: '',
    });
    setPage(0);
  };

  const handleExport = () => {
    if (!data?.items) return;

    const headers = ['Nome', 'Email', 'Cargo', 'Área', 'Tempo de Casa', 'Score Geral', 'Status eNPS'];
    const rows = filteredEmployees.map((emp: any) => [
      emp.nome,
      emp.email,
      emp.cargo_nome || '-',
      emp.area_nome || '-',
      emp.tempo_empresa_nome || '-',
      emp.score_medio_geral ? emp.score_medio_geral.toFixed(2) : '-',
      getEnpsStatus(emp.expectativa_permanencia),
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map((row: string[]) => row.map((cell) => `"${cell}"`).join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `funcionarios_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  };

  const getScoreColor = (score: number | null) => {
    if (!score) return 'default';
    if (score >= 6) return 'success';
    if (score >= 5) return 'warning';
    return 'error';
  };

  const getEnpsStatus = (expectativa: number | null) => {
    if (!expectativa) return 'Sem dados';
    if (expectativa >= 6) return 'Promotor';
    if (expectativa === 5) return 'Neutro';
    return 'Detrator';
  };

  const getEnpsColor = (expectativa: number | null) => {
    if (!expectativa) return 'default';
    if (expectativa >= 6) return 'success';
    if (expectativa === 5) return 'warning';
    return 'error';
  };

  // Usar dados diretamente do backend (já filtrados)
  const filteredEmployees = data?.items || [];

  if (error) {
    return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <TabNavigation />
        <Alert severity="error">
          Erro ao carregar lista de funcionários. Verifique se o backend está rodando.
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <TabNavigation />

      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', mb: 1 }}>
            Funcionários
          </Typography>
          <Typography variant="body1" color="text.secondary">
            {data?.total || 0} colaboradores ativos
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<DownloadIcon />}
          onClick={handleExport}
          disabled={!data?.items || filteredEmployees.length === 0}
        >
          Exportar CSV
        </Button>
      </Box>

      <EmployeeFilterBar filters={filters} onFilterChange={handleFilterChange} onClear={handleClearFilters} />

      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Buscar por nome, e-mail, cargo ou área... (mínimo 2 caracteres)"
          value={searchTerm}
          onChange={handleSearchChange}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon color={searchTerm.length >= 2 ? 'primary' : 'disabled'} />
              </InputAdornment>
            ),
          }}
          helperText={searchTerm.length === 1 ? 'Digite mais 1 caractere para buscar' : ''}
        />
      </Paper>

      {isLoading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
          <CircularProgress size={60} />
        </Box>
      ) : (
        <>
          <TableContainer component={Paper} elevation={3}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 'bold' }}>
                    <TableSortLabel
                      active={orderBy === 'nome'}
                      direction={orderBy === 'nome' ? orderDir : 'asc'}
                      onClick={() => handleSort('nome')}
                    >
                      Nome
                    </TableSortLabel>
                  </TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>E-mail</TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>
                    <TableSortLabel
                      active={orderBy === 'cargo'}
                      direction={orderBy === 'cargo' ? orderDir : 'asc'}
                      onClick={() => handleSort('cargo')}
                    >
                      Cargo
                    </TableSortLabel>
                  </TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>
                    <TableSortLabel
                      active={orderBy === 'area'}
                      direction={orderBy === 'area' ? orderDir : 'asc'}
                      onClick={() => handleSort('area')}
                    >
                      Área
                    </TableSortLabel>
                  </TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>
                    <TableSortLabel
                      active={orderBy === 'tempo'}
                      direction={orderBy === 'tempo' ? orderDir : 'asc'}
                      onClick={() => handleSort('tempo')}
                    >
                      Tempo
                    </TableSortLabel>
                  </TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>
                    <Tooltip title="Score médio geral das 7 dimensões (1-7)">
                      <TableSortLabel
                        active={orderBy === 'score'}
                        direction={orderBy === 'score' ? orderDir : 'asc'}
                        onClick={() => handleSort('score')}
                      >
                        Score
                      </TableSortLabel>
                    </Tooltip>
                  </TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>
                    <Tooltip title="Baseado na Expectativa de Permanência">
                      <span>Status eNPS</span>
                    </Tooltip>
                  </TableCell>
                  <TableCell align="center" sx={{ fontWeight: 'bold' }}>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredEmployees.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={8} align="center" sx={{ py: 8 }}>
                      <Box>
                        <SearchIcon sx={{ fontSize: 60, color: 'text.disabled', mb: 2 }} />
                        <Typography variant="h6" color="text.secondary" gutterBottom>
                          {searchTerm.trim().length >= 2 
                            ? `Nenhum funcionário encontrado para "${searchTerm}"`
                            : isLoading 
                              ? 'Carregando...'
                              : 'Nenhum funcionário encontrado'}
                        </Typography>
                        {searchTerm.trim().length >= 2 && (
                          <Button 
                            variant="outlined" 
                            size="small" 
                            onClick={() => setSearchTerm('')}
                            sx={{ mt: 2 }}
                          >
                            Limpar busca
                          </Button>
                        )}
                      </Box>
                    </TableCell>
                  </TableRow>
                ) : (
                  filteredEmployees.map((employee: any) => (
                    <TableRow key={employee.id} hover>
                      <TableCell>
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                          {employee.nome}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" color="text.secondary">
                          {employee.email}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">{employee.cargo_nome || '-'}</Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">{employee.area_nome || '-'}</Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={employee.tempo_empresa_nome || 'N/A'}
                          size="small"
                          color="primary"
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>
                        {employee.score_medio_geral ? (
                          <Tooltip title={`Score: ${employee.score_medio_geral.toFixed(2)}/7`}>
                            <Chip
                              label={`${employee.score_medio_geral.toFixed(1)}/7`}
                              size="small"
                              color={getScoreColor(employee.score_medio_geral)}
                              sx={{ fontWeight: 'bold', minWidth: '60px' }}
                            />
                          </Tooltip>
                        ) : (
                          <Chip label="Sem dados" size="small" variant="outlined" />
                        )}
                      </TableCell>
                      <TableCell>
                        {employee.expectativa_permanencia ? (
                          <Tooltip title={`Expectativa: ${employee.expectativa_permanencia.toFixed(1)}/7`}>
                            <Chip
                              label={getEnpsStatus(employee.expectativa_permanencia)}
                              size="small"
                              color={getEnpsColor(employee.expectativa_permanencia)}
                              variant="filled"
                              sx={{ fontWeight: 'bold', minWidth: '90px' }}
                            />
                          </Tooltip>
                        ) : (
                          <Chip label="Sem dados" size="small" variant="outlined" />
                        )}
                      </TableCell>
                      <TableCell align="center">
                        <IconButton
                          color="primary"
                          size="small"
                          onClick={() => navigate(`/employees/${employee.id}`)}
                          title="Ver perfil detalhado"
                        >
                          <VisibilityIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>

          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            p: 2,
            borderTop: '1px solid',
            borderColor: 'divider',
            bgcolor: 'background.default'
          }}>
            <Box>
              <Typography variant="body2" color="text.secondary">
                Mostrando <strong>{data?.items?.length || 0}</strong> de <strong>{data?.total || 0}</strong> funcionários
                {searchTerm.trim().length >= 2 && (
                  <Chip 
                    label={`Buscando: "${searchTerm}"`} 
                    size="small" 
                    onDelete={() => setSearchTerm('')}
                    sx={{ ml: 1 }}
                  />
                )}
              </Typography>
            </Box>
            <TablePagination
              component="div"
              count={data?.total || 0}
              page={page}
              onPageChange={handleChangePage}
              rowsPerPage={rowsPerPage}
              onRowsPerPageChange={handleChangeRowsPerPage}
              rowsPerPageOptions={[10, 25, 50, 100]}
              labelRowsPerPage="Por página:"
              labelDisplayedRows={({ from, to, count }) => {
                const totalPages = Math.ceil(count / rowsPerPage);
                const currentPage = page + 1;
                return `Página ${currentPage} de ${totalPages} • ${from}-${to} de ${count}`;
              }}
              sx={{ border: 'none' }}
            />
          </Box>
        </>
      )}
    </Container>
  );
};

export default EmployeeListPage;
