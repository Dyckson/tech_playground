/**
 * Task 7 - Visualização 1: Average Feedback Scores by Department
 * 
 * Gráfico de barras horizontal comparando scores médios entre áreas por dimensão
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
import { getAreasScoresComparison } from '../services/api';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

interface AreaScore {
  area_id: string;
  area_nome: string;
  coordenacao: string;
  gerencia: string;
  diretoria: string;
  total_funcionarios: number;
  dimensoes: Array<{
    dimensao: string;
    score_medio: number;
    total_respostas: number;
  }>;
  score_medio_geral?: number;
}

interface AreasScoresData {
  areas: AreaScore[];
  total_areas: number;
}

const DIMENSOES = [
  'Todas as Dimensões',
  'Aprendizado e Desenvolvimento',
  'Interesse no Cargo',
  'Interação com Gestor',
  'Feedback',
  'Expectativa de Permanência',
  'Contribuição',
  'Clareza sobre Possibilidades de Carreira',
];

const getBarColor = (score: number) => {
  if (score >= 6) return 'rgba(76, 175, 80, 0.8)';
  if (score >= 4.5) return 'rgba(255, 152, 0, 0.8)';
  return 'rgba(244, 67, 54, 0.8)';
};

export default function AreasScoresComparison() {
  const [data, setData] = useState<AreasScoresData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDimensao, setSelectedDimensao] = useState('Todas as Dimensões');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await getAreasScoresComparison();
      setData(response);
    } catch (err) {
      setError('Erro ao carregar dados de comparação de áreas');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const prepareChartData = () => {
    if (!data) return { labels: [], datasets: [] };

    let chartItems;

    if (selectedDimensao === 'Todas as Dimensões') {
      chartItems = data.areas
        .map((area) => {
          const scoreGeral =
            area.score_medio_geral ||
            area.dimensoes.reduce((sum, d) => sum + d.score_medio, 0) / area.dimensoes.length;
          return {
            area: area.area_nome,
            score: scoreGeral,
            funcionarios: area.total_funcionarios,
            hierarquia: `${area.diretoria} › ${area.gerencia} › ${area.coordenacao}`,
          };
        })
        .sort((a, b) => b.score - a.score)
        .slice(0, 10);
    } else {
      chartItems = data.areas
        .map((area) => {
          const dimensao = area.dimensoes.find((d) => d.dimensao === selectedDimensao);
          return {
            area: area.area_nome,
            score: dimensao?.score_medio || 0,
            funcionarios: area.total_funcionarios,
            respostas: dimensao?.total_respostas || 0,
            hierarquia: `${area.diretoria} › ${area.gerencia} › ${area.coordenacao}`,
          };
        })
        .filter((item) => item.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, 10);
    }

    const backgroundColors = chartItems.map((item) => getBarColor(item.score));

    return {
      labels: chartItems.map((item) => item.area),
      datasets: [
        {
          label: 'Score Médio',
          data: chartItems.map((item) => item.score),
          backgroundColor: backgroundColors,
          borderColor: backgroundColors.map((color) => color.replace('0.8', '1')),
          borderWidth: 1,
        },
      ],
    };
  };

  const chartData = prepareChartData();

  const getInsights = () => {
    if (!chartData.datasets.length || !chartData.labels.length) return null;

    const scores = chartData.datasets[0].data as number[];
    const labels = chartData.labels as string[];

    const melhorScore = scores[0];
    const piorScore = scores[scores.length - 1];
    const mediaGeral = scores.reduce((sum, s) => sum + s, 0) / scores.length;

    return {
      melhorArea: labels[0],
      melhorScore,
      piorArea: labels[labels.length - 1],
      piorScore,
      mediaGeral: mediaGeral.toFixed(2),
      diferenca: (melhorScore - piorScore).toFixed(2),
    };
  };

  const insights = getInsights();

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

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h5" gutterBottom>
            📊 Comparação de Scores por Área
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Top 10 áreas por desempenho médio
          </Typography>
        </Box>

        <FormControl sx={{ minWidth: 300 }}>
          <InputLabel>Dimensão</InputLabel>
          <Select
            value={selectedDimensao}
            label="Dimensão"
            onChange={(e) => setSelectedDimensao(e.target.value)}
          >
            {DIMENSOES.map((dim) => (
              <MenuItem key={dim} value={dim}>
                {dim}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {insights && (
        <Box display="flex" gap={2} mb={3} flexWrap="wrap">
          <Chip
            label={`🏆 Melhor: ${insights.melhorArea} (${insights.melhorScore.toFixed(2)})`}
            color="success"
            variant="outlined"
          />
          <Chip
            label={`⚠️ Menor: ${insights.piorArea} (${insights.piorScore.toFixed(2)})`}
            color="error"
            variant="outlined"
          />
          <Chip
            label={`📊 Média Geral: ${insights.mediaGeral}`}
            color="primary"
            variant="outlined"
          />
          <Chip
            label={`📈 Diferença: ${insights.diferenca} pontos`}
            color="info"
            variant="outlined"
          />
        </Box>
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
                display: false,
              },
              tooltip: {
                callbacks: {
                  label: (context) => {
                    return `Score: ${context.parsed.x?.toFixed(2) || 0} / 7.0`;
                  },
                },
              },
            },
            scales: {
              x: {
                min: 0,
                max: 7,
                title: {
                  display: true,
                  text: 'Score Médio',
                },
              },
              y: {
                title: {
                  display: true,
                  text: 'Área',
                },
              },
            },
          }}
        />
      </Box>

      <Box display="flex" gap={2} mt={2} justifyContent="center">
        <Chip
          icon={<Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: '#4caf50' }} />}
          label="Excelente (≥ 6.0)"
          size="small"
          variant="outlined"
        />
        <Chip
          icon={<Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: '#ff9800' }} />}
          label="Bom (4.5 - 5.9)"
          size="small"
          variant="outlined"
        />
        <Chip
          icon={<Box sx={{ width: 12, height: 12, borderRadius: '50%', bgcolor: '#f44336' }} />}
          label="Precisa Atenção (< 4.5)"
          size="small"
          variant="outlined"
        />
      </Box>

      <Alert severity="info" sx={{ mt: 3 }}>
        <Typography variant="body2">
          <strong>O que este gráfico revela:</strong>
        </Typography>
        <ul style={{ marginTop: 8, paddingLeft: 20 }}>
          <li>
            <strong>Áreas com melhor desempenho:</strong> Identificar departamentos com scores mais
            altos para reconhecimento e benchmarking
          </li>
          <li>
            <strong>Áreas que precisam atenção:</strong> Departamentos com scores baixos podem
            necessitar intervenção, treinamento ou mudanças de gestão
          </li>
          <li>
            <strong>Variação entre áreas:</strong> Grande diferença entre melhor e pior área
            indica disparidade nas condições de trabalho ou liderança
          </li>
          <li>
            <strong>Filtro por dimensão:</strong> Permite identificar pontos fortes e fracos
            específicos de cada área
          </li>
        </ul>
      </Alert>
    </Paper>
  );
}
