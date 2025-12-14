import { Card, CardHeader, CardContent, CircularProgress, Alert, Box, Typography } from '@mui/material';
import { Star as StarIcon } from '@mui/icons-material';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';
import type { SatisfactionScores } from '@/types/api.types';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

interface SatisfactionScoresChartProps {
  data: SatisfactionScores;
  isLoading?: boolean;
  error?: Error | null;
}

const SatisfactionScoresChart: React.FC<SatisfactionScoresChartProps> = ({
  data,
  isLoading,
  error,
}) => {
  if (isLoading) {
    return (
      <Card sx={{ height: '100%' }}>
        <CardContent sx={{ textAlign: 'center', py: 5 }}>
          <CircularProgress />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 3 }}>
            Carregando scores de satisfação...
          </Typography>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card sx={{ height: '100%' }}>
        <CardContent>
          <Alert severity="error">Erro ao carregar dados: {error.message}</Alert>
        </CardContent>
      </Card>
    );
  }

  const dimensions = [
    { key: 'comunicacao', label: 'Comunicação' },
    { key: 'desenvolvimentoProfissional', label: 'Desenvolvimento' },
    { key: 'equilibrioVidaPessoal', label: 'Equilíbrio Vida/Trabalho' },
    { key: 'lideranca', label: 'Liderança' },
    { key: 'reconhecimento', label: 'Reconhecimento' },
    { key: 'remuneracaoBeneficios', label: 'Remuneração' },
    { key: 'trabalhoEquipe', label: 'Trabalho em Equipe' },
  ];

  const chartData = {
    labels: dimensions.map((d) => d.label),
    datasets: [
      {
        label: 'Score Médio',
        data: dimensions.map((d) => data[d.key as keyof SatisfactionScores]),
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(54, 162, 235, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(54, 162, 235, 1)',
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const value = context.parsed.r || 0;
            return `Score: ${value.toFixed(2)}/5`;
          },
        },
      },
    },
    scales: {
      r: {
        beginAtZero: true,
        max: 5,
        min: 0,
        ticks: {
          stepSize: 1,
        },
        pointLabels: {
          font: {
            size: 11,
          },
        },
      },
    },
  };

  return (
    <Card elevation={2} sx={{ height: '100%' }}>
      <CardHeader
        avatar={<StarIcon />}
        title="Scores de Satisfação por Dimensão"
        titleTypographyProps={{ variant: 'h6' }}
      />
      <CardContent>
        <Box sx={{ height: 400 }}>
          <Radar data={chartData} options={options} />
        </Box>
        <Box sx={{ mt: 3 }}>
          <Typography variant="caption" color="text.secondary" display="block" textAlign="center">
            Escala Likert: 1 (Discordo totalmente) a 5 (Concordo totalmente)
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default SatisfactionScoresChart;
