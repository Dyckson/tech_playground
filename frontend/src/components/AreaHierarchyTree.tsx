import { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Chip,
  Collapse,
  IconButton,
} from '@mui/material';
import {
  ExpandMore as ExpandMoreIcon,
  ChevronRight as ChevronRightIcon,
  Business as BusinessIcon,
  AccountTree as AccountTreeIcon,
  ViewList as ViewListIcon,
  Apartment as ApartmentIcon,
} from '@mui/icons-material';
import { useAreaHierarchy, useAreaEmployeeCount } from '../hooks/useAreas';

interface AreaTreeNode {
  id: string;
  nome: string;
  tipo: 'diretoria' | 'gerencia' | 'coordenacao' | 'area';
  gerencias?: AreaTreeNode[];
  coordenacoes?: AreaTreeNode[];
  areas?: AreaTreeNode[];
}

interface TreeNodeProps {
  node: AreaTreeNode;
  level: number;
  employeeCount: Map<string, number>;
  onAreaClick?: (areaId: string) => void;
}

const TreeNode: React.FC<TreeNodeProps> = ({ node, level, employeeCount, onAreaClick }) => {
  const [expanded, setExpanded] = useState(level === 0); // Diretorias expandidas por padrão

  const hasChildren =
    (node.gerencias && node.gerencias.length > 0) ||
    (node.coordenacoes && node.coordenacoes.length > 0) ||
    (node.areas && node.areas.length > 0);

  const getIcon = () => {
    switch (node.tipo) {
      case 'diretoria':
        return <BusinessIcon sx={{ fontSize: 20 }} />;
      case 'gerencia':
        return <AccountTreeIcon sx={{ fontSize: 20 }} />;
      case 'coordenacao':
        return <ViewListIcon sx={{ fontSize: 20 }} />;
      case 'area':
        return <ApartmentIcon sx={{ fontSize: 20 }} />;
    }
  };

  const getColor = () => {
    switch (node.tipo) {
      case 'diretoria':
        return '#1976d2';
      case 'gerencia':
        return '#2e7d32';
      case 'coordenacao':
        return '#ed6c02';
      case 'area':
        return '#9c27b0';
    }
  };

  const totalEmployees = node.tipo === 'area' ? employeeCount.get(node.id) || 0 : null;

  const handleClick = () => {
    if (hasChildren) {
      setExpanded(!expanded);
    }
    if (node.tipo === 'area' && onAreaClick) {
      onAreaClick(node.id);
    }
  };

  return (
    <Box>
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          py: 1,
          pl: level * 3,
          pr: 2,
          cursor: hasChildren || node.tipo === 'area' ? 'pointer' : 'default',
          '&:hover': {
            bgcolor: 'action.hover',
          },
          borderRadius: 1,
        }}
        onClick={handleClick}
      >
        {hasChildren ? (
          <IconButton size="small" sx={{ mr: 1 }}>
            {expanded ? <ExpandMoreIcon /> : <ChevronRightIcon />}
          </IconButton>
        ) : (
          <Box sx={{ width: 40 }} />
        )}

        <Box
          sx={{
            bgcolor: `${getColor()}15`,
            p: 0.5,
            borderRadius: 1,
            mr: 1.5,
            display: 'flex',
            alignItems: 'center',
          }}
        >
          {getIcon()}
        </Box>

        <Typography
          variant="body1"
          sx={{
            flex: 1,
            fontWeight: node.tipo === 'diretoria' ? 600 : 500,
            color: node.tipo === 'area' ? 'primary.main' : 'text.primary',
          }}
        >
          {node.nome}
        </Typography>

        {totalEmployees !== null && (
          <Chip
            label={`${totalEmployees} funcionários`}
            size="small"
            sx={{
              bgcolor: `${getColor()}15`,
              color: getColor(),
              fontWeight: 600,
            }}
          />
        )}
      </Box>

      {hasChildren && (
        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <Box>
            {node.gerencias?.map((gerencia) => (
              <TreeNode
                key={gerencia.id}
                node={gerencia}
                level={level + 1}
                employeeCount={employeeCount}
                onAreaClick={onAreaClick}
              />
            ))}
            {node.coordenacoes?.map((coordenacao) => (
              <TreeNode
                key={coordenacao.id}
                node={coordenacao}
                level={level + 1}
                employeeCount={employeeCount}
                onAreaClick={onAreaClick}
              />
            ))}
            {node.areas?.map((area) => (
              <TreeNode
                key={area.id}
                node={area}
                level={level + 1}
                employeeCount={employeeCount}
                onAreaClick={onAreaClick}
              />
            ))}
          </Box>
        </Collapse>
      )}
    </Box>
  );
};

interface AreaHierarchyTreeProps {
  empresaId?: string;
  onAreaClick?: (areaId: string) => void;
}

const AreaHierarchyTree: React.FC<AreaHierarchyTreeProps> = ({ empresaId, onAreaClick }) => {
  const { data: hierarchy, isLoading: hierarchyLoading } = useAreaHierarchy(empresaId);
  const { data: contagem, isLoading: contagemLoading } = useAreaEmployeeCount(empresaId);

  if (hierarchyLoading || contagemLoading) {
    return (
      <Card elevation={3}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 300 }}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    );
  }

  if (!hierarchy || hierarchy.length === 0) {
    return (
      <Card elevation={3}>
        <CardContent>
          <Typography color="text.secondary">Nenhuma estrutura hierárquica encontrada</Typography>
        </CardContent>
      </Card>
    );
  }

  // Criar mapa de contagem de funcionários por área
  const employeeCountMap = new Map<string, number>();
  contagem?.forEach((item) => {
    employeeCountMap.set(item.area_id, item.total_funcionarios);
  });

  return (
    <Card elevation={3}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold', mb: 3 }}>
          Estrutura Organizacional
        </Typography>

        <Box>
          {hierarchy.map((diretoria) => (
            <TreeNode
              key={diretoria.id}
              node={diretoria}
              level={0}
              employeeCount={employeeCountMap}
              onAreaClick={onAreaClick}
            />
          ))}
        </Box>

        <Box sx={{ mt: 3, pt: 2, borderTop: 1, borderColor: 'divider' }}>
          <Typography variant="caption" color="text.secondary" display="block" gutterBottom>
            Legenda:
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <BusinessIcon sx={{ fontSize: 16, color: '#1976d2' }} />
              <Typography variant="caption">Diretoria</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <AccountTreeIcon sx={{ fontSize: 16, color: '#2e7d32' }} />
              <Typography variant="caption">Gerência</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <ViewListIcon sx={{ fontSize: 16, color: '#ed6c02' }} />
              <Typography variant="caption">Coordenação</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <ApartmentIcon sx={{ fontSize: 16, color: '#9c27b0' }} />
              <Typography variant="caption">Área</Typography>
            </Box>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default AreaHierarchyTree;
