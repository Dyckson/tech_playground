import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  Container,
  Grid,
  Box,
  Typography,
  CircularProgress,
  Alert,
  AlertTitle,
  Button,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Divider,
  Chip,
} from '@mui/material';
import { ArrowBack, Comment as CommentIcon, History as HistoryIcon } from '@mui/icons-material';
import axios from 'axios';
import EmployeeProfileCard from '../components/EmployeeProfileCard';
import EmployeeRadarComparison from '../components/EmployeeRadarComparison';

const EmployeeDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { from, areaId, areaName } = (location.state || {}) as { from?: string; areaId?: string; areaName?: string };

  const { data, isLoading, error } = useQuery({
    queryKey: ['employee-detail', id],
    queryFn: async () => {
      const { data } = await axios.get(`http://localhost:9876/api/v1/funcionarios/${id}/detailed-profile`);
      return data;
    },
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2 }} color="text.secondary">
            Carregando perfil do funcionário...
          </Typography>
        </Box>
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Alert severity="error">
          <AlertTitle>Erro ao Carregar Perfil</AlertTitle>
          Não foi possível carregar os dados do funcionário.
        </Alert>
        <Button startIcon={<ArrowBack />} onClick={() => navigate('/')} sx={{ mt: 2 }}>
          Voltar ao Dashboard
        </Button>
      </Container>
    );
  }

  const { employee, analytics } = data;

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Button 
        startIcon={<ArrowBack />} 
        onClick={() => from === 'area' && areaId ? navigate(`/areas/${areaId}`) : navigate('/employees')} 
        sx={{ mb: 3 }}
      >
        {from === 'area' && areaName ? `Voltar para ${areaName}` : 'Voltar para Funcionários'}
      </Button>

      <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', mb: 3 }}>
        Perfil Detalhado do Funcionário
      </Typography>

      <Grid container spacing={3}>
        {/* Perfil do Funcionário */}
        <Grid item xs={12} lg={4}>
          <EmployeeProfileCard employee={employee} />
        </Grid>

        {/* Radar de Comparação */}
        <Grid item xs={12} lg={8}>
          <EmployeeRadarComparison
            comparison={analytics.comparison}
            employeeName={employee.nome}
          />
        </Grid>

        {/* Histórico de Avaliações */}
        <Grid item xs={12} md={6}>
          <Card elevation={3}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <HistoryIcon color="primary" />
                <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                  Histórico de Avaliações
                </Typography>
              </Box>

              {analytics.history.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  Nenhuma avaliação registrada.
                </Typography>
              ) : (
                <List>
                  {analytics.history.map((item: any, index: number) => (
                    <Box key={index}>
                      <ListItem alignItems="flex-start" sx={{ px: 0 }}>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                              <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                                {item.periodo_avaliacao || 'Avaliação'}
                              </Typography>
                              <Chip
                                label={`Score: ${item.score_medio_geral || 0}/7`}
                                size="small"
                                color="primary"
                              />
                            </Box>
                          }
                          secondary={
                            <>
                              <Typography variant="caption" color="text.secondary" display="block">
                                {new Date(item.data_avaliacao).toLocaleDateString('pt-BR')}
                              </Typography>
                              {item.comentario_geral && (
                                <Typography variant="body2" sx={{ mt: 0.5 }}>
                                  {item.comentario_geral}
                                </Typography>
                              )}
                              <Typography variant="caption" color="text.secondary">
                                {item.total_dimensoes} dimensões avaliadas
                              </Typography>
                            </>
                          }
                        />
                      </ListItem>
                      {index < analytics.history.length - 1 && <Divider />}
                    </Box>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Comentários Detalhados */}
        <Grid item xs={12} md={6}>
          <Card elevation={3}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <CommentIcon color="primary" />
                <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                  Comentários Detalhados
                </Typography>
              </Box>

              {analytics.comments.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  Nenhum comentário registrado.
                </Typography>
              ) : (
                <List>
                  {analytics.comments.map((comment: any, index: number) => (
                    <Box key={index}>
                      <ListItem alignItems="flex-start" sx={{ px: 0 }}>
                        <ListItemText
                          primary={
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                              <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                                {comment.dimensao}
                              </Typography>
                              <Chip label={`${comment.score}/7`} size="small" color="secondary" />
                            </Box>
                          }
                          secondary={
                            <>
                              <Typography variant="body2" sx={{ mt: 0.5 }}>
                                {comment.comentario}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                {new Date(comment.data_avaliacao).toLocaleDateString('pt-BR')}
                              </Typography>
                            </>
                          }
                        />
                      </ListItem>
                      {index < analytics.comments.length - 1 && <Divider />}
                    </Box>
                  ))}
                </List>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Resumo Estatístico */}
        <Grid item xs={12}>
          <Card elevation={3} sx={{ bgcolor: 'primary.main', color: 'white' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                Resumo Estatístico
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={4}>
                  <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                    {analytics.summary.total_evaluations}
                  </Typography>
                  <Typography variant="body2">Avaliações Realizadas</Typography>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                    {analytics.summary.dimensions_evaluated}
                  </Typography>
                  <Typography variant="body2">Dimensões Avaliadas</Typography>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Typography variant="h3" sx={{ fontWeight: 'bold' }}>
                    {analytics.comments.length}
                  </Typography>
                  <Typography variant="body2">Comentários Registrados</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default EmployeeDetailPage;
