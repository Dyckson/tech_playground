import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  CircularProgress,
  Box,
  IconButton,
  Chip,
} from '@mui/material';
import { Visibility as VisibilityIcon } from '@mui/icons-material';
import axios from 'axios';

const EmployeeListTable = () => {
  const navigate = useNavigate();
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const { data, isLoading } = useQuery({
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

  const handleViewEmployee = (id: string) => {
    navigate(`/employee/${id}`);
  };

  if (isLoading) {
    return (
      <Card elevation={3}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
          Lista de Funcionários
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          Clique no ícone para ver o perfil detalhado do funcionário
        </Typography>

        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 'bold' }}>Nome</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Cargo</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Área</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Localidade</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Tempo de Casa</TableCell>
                <TableCell align="center" sx={{ fontWeight: 'bold' }}>Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data?.items.map((employee: any) => (
                <TableRow
                  key={employee.id}
                  hover
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell>{employee.nome}</TableCell>
                  <TableCell>
                    <Chip label={employee.cargo_nome} size="small" color="primary" variant="outlined" />
                  </TableCell>
                  <TableCell>{employee.area_nome}</TableCell>
                  <TableCell>{employee.localidade_nome}</TableCell>
                  <TableCell>
                    <Chip label={employee.tempo_empresa_nome} size="small" />
                  </TableCell>
                  <TableCell align="center">
                    <IconButton
                      size="small"
                      color="primary"
                      onClick={() => handleViewEmployee(employee.id)}
                      title="Ver perfil detalhado"
                    >
                      <VisibilityIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <TablePagination
          rowsPerPageOptions={[5, 10, 25, 50]}
          component="div"
          count={data?.total || 0}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
          labelRowsPerPage="Linhas por página:"
          labelDisplayedRows={({ from, to, count }) => `${from}-${to} de ${count}`}
        />
      </CardContent>
    </Card>
  );
};

export default EmployeeListTable;
