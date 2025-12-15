/**
 * Task 7 - Visualização 2: eNPS Comparison by Department
 * 
 * Ranking de áreas por eNPS (Employee Net Promoter Score)
 */

import { useEffect, useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  CircularProgress,
  Alert,
  Chip,
  Card,
  CardContent,
  Grid,
} from '@mui/material';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { getAreasEnpsComparison } from '../services/api';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface AreaEnps {
  area_id: string;
  area_nome: string;
  coordenacao: string;
  gerencia: string;
  diretoria: string;
  promotores: number;
  neutros: number;
  detratores: number;
  promotores_percentual: number;
  neutros_percentual: number;
  detratores_percentual: number;
  enps_score: number;
  total_respostas: number;
}

interface AreasEnpsData {
  areas: AreaEnps[];
  total_areas: number;
  melhor_area: AreaEnps;
  pior_area: AreaEnps;
  enps_medio: number;
}

export default function AreasEnpsComparison() {
  const [data, setData] = useState<AreasEnpsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDiretoria, setSelectedDiretoria] = useState('Todas');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getAreasEnpsComparison();
      setData(response);
    } catch (err) {
      setError('Erro ao carregar dados de eNPS por área');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getDiretorias = () => {
    if (!data) return [];
    const diretorias = new Set(data.areas.map((a) => a.diretoria));
    return ['Todas', ...Array.from(diretorias).sort()];
  };

  const prepareChartData = () => {
    if (!data) return { labels: [], datasets: [] };

    let filteredAreas = data.areas;

    if (selectedDiretoria !== 'Todas') {
      filteredAreas = filteredAreas.filter((a) => a.diretoria === selectedDiretoria);
    }

    const chartItems = filteredAreas
      .map((area) => ({
        area: area.area_nome,
        promotores: area.promotores_percentual,
        neutros: area.neutros_percentual,
        detratores: area.detratores_percentual,
        enps: area.enps_score,
        hierarquia: `${area.diretoria} › ${area.gerencia} › ${area.coordenacao}`,
        total_respostas: area.total_respostas,
        promotores_count: area.promotores,
        neutros_count: area.neutros,
        detratores_count: area.detratores,
      }))
      .sort((a, b) => b.enps - a.enps)
      .slice(0, 10);

    return {
      labels: chartItems.map((item) => item.area),
      datasets: [
        {
          label: 'Promotores (6-7)',
          data: chartItems.map((item) => item.promotores),
          backgroundColor: 'rgba(76, 175, 80, 0.8)',
          borderColor: 'rgba(76, 175, 80, 1)',
          borderWidth: 1,
        },
        {
          label: 'Neutros (5)',
          data: chartItems.map((item) => item.neutros),
          backgroundColor: 'rgba(255, 152, 0, 0.8)',
          borderColor: 'rgba(255, 152, 0, 1)',
          borderWidth: 1,
        },
        {
          label: 'Detratores (1-4)',
          data: chartItems.map((item) => item.detratores),
          backgroundColor: 'rgba(244, 67, 54, 0.8)',
          borderColor: 'rgba(244, 67, 54, 1)',
          borderWidth: 1,
        },
      ],
    };
  };

  const chartData = prepareChartData();

  const getEnpsCategory = (score: number) => {
    if (score >= 50) return { label: 'Excelente', color: '#4caf50' };
    if (score >= 20) return { label: 'Muito Bom', color: '#8bc34a' };
    if (score >= 0) return { label: 'Bom', color: '#ff9800' };
    if (score >= -20) return { label: 'Regular', color: '#ff5722' };
    return { label: 'Crítico', color: '#f44336' };
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        {error}
      </Alert>
    );
  }

  const diretorias = getDiretorias();

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h5" gutterBottom>
            🎯 Ranking de eNPS por Área
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Top 10 áreas por engajamento (eNPS)
          </Typography>
        </Box>

        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Diretoria</InputLabel>
          <Select
            value={selectedDiretoria}
            label="Diretoria"
            onChange={(e) => setSelectedDiretoria(e.target.value)}
          >
            {diretorias.map((dir) => (
              <MenuItem key={dir} value={dir}>
                {dir}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {data && data.melhor_area && data.pior_area && (
        <Grid container spacing={2} mb={3}>
          <Grid item xs={12} md={4}>
            <Card elevation={2} sx={{ bgcolor: '#e8f5e9' }}>
              <CardContent>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <TrendingUpIcon color="success" />
                  <Typography variant="h6" color="success.main">
                    Melhor Área
                  </Typography>
                </Box>
                <Typography variant="h4" gutterBottom>
                  {data.melhor_area.area_nome || 'N/A'}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {data.melhor_area.diretoria || ''} › {data.melhor_area.gerencia || ''}
                </Typography>
                <Chip
                  label={`eNPS: ${(data.melhor_area.enps_score || 0).toFixed(1)}`}
                  color="success"
                  size="small"
                />
                <Typography variant="caption" display="block" mt={1}>
                  {(data.melhor_area.promotores_percentual || 0).toFixed(0)}% promotores
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card elevation={2} sx={{ bgcolor: '#e3f2fd' }}>
              <CardContent>
                <Typography variant="h6" color="primary" gutterBottom>
                  Média Geral
                </Typography>
                <Typography variant="h4" gutterBottom>
                  {(data.enps_medio || 0).toFixed(1)}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Todas as {data.total_areas || 0} áreas
                </Typography>
                <Chip
                  label={getEnpsCategory(data.enps_medio || 0).label}
                  sx={{ bgcolor: getEnpsCategory(data.enps_medio || 0).color, color: 'white' }}
                  size="small"
                />
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card elevation={2} sx={{ bgcolor: '#ffebee' }}>
              <CardContent>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <TrendingDownIcon color="error" />
                  <Typography variant="h6" color="error.main">
                    Área que Precisa Atenção
                  </Typography>
                </Box>
                <Typography variant="h4" gutterBottom>
                  {data.pior_area.area_nome || 'N/A'}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {data.pior_area.diretoria || ''} › {data.pior_area.gerencia || ''}
                </Typography>
                <Chip
                  label={`eNPS: ${(data.pior_area.enps_score || 0).toFixed(1)}`}
                  color="error"
                  size="small"
                />
                <Typography variant="caption" display="block" mt={1}>
                  {(data.pior_area.detratores_percentual || 0).toFixed(0)}% detratores
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Box sx={{ height: 400, position: 'relative' }}>
        <Bar
          data={chartData}
          options={{
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'top',
              },
              tooltip: {
                callbacks: {
                  label: (context) => {
                    return `${context.dataset.label}: ${context.parsed.x?.toFixed(1) || 0}%`;
                  },
                },
              },
            },
            scales: {
              x: {
                stacked: true,
                min: 0,
                max: 100,
                title: {
                  display: true,
                  text: 'Percentual (%)',
                },
              },
              y: {
                stacked: true,
                title: {
                  display: true,
                  text: 'Área',
                },
              },
            },
          }}
        />
      </Box>

      <Alert severity="info" sx={{ mt: 3 }}>
        <Typography variant="body2" gutterBottom>
          <strong>Como interpretar o eNPS:</strong>
        </Typography>
        <ul style={{ marginTop: 8, paddingLeft: 20, marginBottom: 8 }}>
          <li>
            <strong>eNPS = % Promotores - % Detratores</strong> (varia de -100 a +100)
          </li>
          <li>
            <strong>Promotores (6-7):</strong> Funcionários altamente engajados
          </li>
          <li>
            <strong>Neutros (5):</strong> Funcionários satisfeitos mas não entusiastas
          </li>
          <li>
            <strong>Detratores (1-4):</strong> Funcionários insatisfeitos, risco de turnover
          </li>
        </ul>
        <Typography variant="body2">
          <strong>Possíveis razões para diferenças entre áreas:</strong>
        </Typography>
        <ul style={{ marginTop: 8, paddingLeft: 20 }}>
          <li>
            <strong>Liderança:</strong> Gestores com melhor comunicação geram maior engajamento
          </li>
          <li>
            <strong>Desenvolvimento:</strong> Áreas com programas de treinamento têm eNPS mais alto
          </li>
          <li>
            <strong>Carga de trabalho:</strong> Equipes sobrecarregadas apresentam mais detratores
          </li>
          <li>
            <strong>Cultura:</strong> Ambiente tóxico ou falta de reconhecimento reduz eNPS
          </li>
        </ul>
      </Alert>

      <Box display="flex" gap={1} mt={2} justifyContent="center" flexWrap="wrap">
        <Chip
          label="Excelente (≥ 50)"
          sx={{ bgcolor: '#4caf50', color: 'white' }}
          size="small"
        />
        <Chip
          label="Muito Bom (20-49)"
          sx={{ bgcolor: '#8bc34a', color: 'white' }}
          size="small"
        />
        <Chip label="Bom (0-19)" sx={{ bgcolor: '#ff9800', color: 'white' }} size="small" />
        <Chip
          label="Regular (-20 a -1)"
          sx={{ bgcolor: '#ff5722', color: 'white' }}
          size="small"
        />
        <Chip label="Crítico (< -20)" sx={{ bgcolor: '#f44336', color: 'white' }} size="small" />
      </Box>
    </Paper>
  );
}
