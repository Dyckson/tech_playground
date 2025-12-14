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
} from '@mui/material';
import { Search as SearchIcon, Visibility as VisibilityIcon } from '@mui/icons-material';
import axios from 'axios';
import TabNavigation from '../components/TabNavigation';

const EmployeeListPage = () => {
  const navigate = useNavigate();
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [searchTerm, setSearchTerm] = useState('');

  const { data, isLoading, error } = useQuery({
    queryKey: ['employees', page + 1, rowsPerPage],
    queryFn: async () => {
      const { data } = await axios.get('http://localhost:9876/api/v1/funcionarios', {
        params: {
          page: page + 1,
          page_size: rowsPerPage,
        },
      });
      return data;
    },
  });

  const handleChangePage = (_event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const filteredEmployees = data?.items?.filter((employee: any) =>
    employee.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
    employee.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    employee.cargo_nome?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    employee.area_nome?.toLowerCase().includes(searchTerm.toLowerCase())
  ) || [];

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

      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', mb: 1 }}>
          Funcionários
        </Typography>
        <Typography variant="body1" color="text.secondary">
          {data?.total || 0} colaboradores ativos
        </Typography>
      </Box>

      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Buscar por nome, e-mail, cargo ou área..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
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
                  <TableCell sx={{ fontWeight: 'bold' }}>Nome</TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>E-mail</TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>Cargo</TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>Área</TableCell>
                  <TableCell sx={{ fontWeight: 'bold' }}>Tempo</TableCell>
                  <TableCell align="center" sx={{ fontWeight: 'bold' }}>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredEmployees.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center" sx={{ py: 4 }}>
                      <Typography variant="body2" color="text.secondary">
                        {searchTerm ? 'Nenhum funcionário encontrado' : 'Nenhum dado disponível'}
                      </Typography>
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

          <TablePagination
            component="div"
            count={data?.total || 0}
            page={page}
            onPageChange={handleChangePage}
            rowsPerPage={rowsPerPage}
            onRowsPerPageChange={handleChangeRowsPerPage}
            rowsPerPageOptions={[5, 10, 25, 50]}
            labelRowsPerPage="Linhas por página:"
            labelDisplayedRows={({ from, to, count }) => `${from}-${to} de ${count}`}
          />
        </>
      )}
    </Container>
  );
};

export default EmployeeListPage;
