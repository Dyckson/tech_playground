import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Chip,
  SelectChangeEvent,
  TextField,
} from '@mui/material';
import { FilterList as FilterIcon, Clear as ClearIcon } from '@mui/icons-material';
import axios from 'axios';

export interface FilterValues {
  cargos: string[];
  areas: string[];
  temposCasa: string[];
  scoreMin: string;
  scoreMax: string;
  enpsStatus: string;
}

interface FilterOptions {
  cargos: Array<{ id: string; nome: string }>;
  areas: Array<{ id: string; nome: string }>;
  localidades: Array<{ id: string; nome: string }>;
}

interface Props {
  filters: FilterValues;
  onFilterChange: (filters: FilterValues) => void;
  onClear: () => void;
}

const EmployeeFilterBar = ({ filters, onFilterChange, onClear }: Props) => {
  const [options, setOptions] = useState<FilterOptions>({
    cargos: [],
    areas: [],
    localidades: [],
  });

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const { data } = await axios.get('http://localhost:9876/api/v1/funcionarios/filtros');
        setOptions(data);
      } catch (error) {
        console.error('Erro ao carregar opções de filtro:', error);
      }
    };
    fetchOptions();
  }, []);

  const handleChange = (field: keyof FilterValues) => (
    event: SelectChangeEvent<string | string[]>
  ) => {
    const value = event.target.value;
    onFilterChange({
      ...filters,
      [field]: value,
    });
  };

  const handleTextChange = (field: keyof FilterValues) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.value;
    onFilterChange({
      ...filters,
      [field]: value,
    });
  };

  const hasActiveFilters =
    filters.cargos.length > 0 ||
    filters.areas.length > 0 ||
    filters.temposCasa.length > 0 ||
    filters.scoreMin !== '' ||
    filters.scoreMax !== '' ||
    filters.enpsStatus !== '';

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
        <FilterIcon color="primary" />
        <Box sx={{ flexGrow: 1, fontWeight: 'bold', fontSize: '1.1rem' }}>
          Filtros Avançados
        </Box>
        {hasActiveFilters && (
          <Button
            startIcon={<ClearIcon />}
            onClick={onClear}
            variant="outlined"
            size="small"
            color="secondary"
          >
            Limpar Filtros
          </Button>
        )}
      </Box>

      <Grid container spacing={2}>
        <Grid item xs={12} md={6} lg={3}>
          <FormControl fullWidth size="small">
            <InputLabel>Cargo</InputLabel>
            <Select
              multiple
              value={filters.cargos}
              onChange={handleChange('cargos')}
              label="Cargo"
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {(selected as string[]).map((value) => {
                    const cargo = options.cargos.find((c) => c.id === value);
                    return <Chip key={value} label={cargo?.nome || value} size="small" />;
                  })}
                </Box>
              )}
            >
              {options.cargos.map((cargo) => (
                <MenuItem key={cargo.id} value={cargo.id}>
                  {cargo.nome}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} md={6} lg={3}>
          <FormControl fullWidth size="small">
            <InputLabel>Área</InputLabel>
            <Select
              multiple
              value={filters.areas}
              onChange={handleChange('areas')}
              label="Área"
              renderValue={(selected) => (
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {(selected as string[]).map((value) => {
                    const area = options.areas.find((a) => a.id === value);
                    return <Chip key={value} label={area?.nome || value} size="small" />;
                  })}
                </Box>
              )}
            >
              {options.areas.map((area) => (
                <MenuItem key={area.id} value={area.id}>
                  {area.nome}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} md={6} lg={2}>
          <FormControl fullWidth size="small">
            <InputLabel>Status eNPS</InputLabel>
            <Select
              value={filters.enpsStatus}
              onChange={handleChange('enpsStatus')}
              label="Status eNPS"
            >
              <MenuItem value="">Todos</MenuItem>
              <MenuItem value="promotor">Promotores (6-7)</MenuItem>
              <MenuItem value="neutro">Neutros (5)</MenuItem>
              <MenuItem value="detrator">Detratores (1-4)</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={6} md={3} lg={2}>
          <TextField
            fullWidth
            size="small"
            type="number"
            label="Score Mínimo"
            value={filters.scoreMin}
            onChange={handleTextChange('scoreMin')}
            inputProps={{ min: 1, max: 7, step: 0.1 }}
            helperText="1-7"
          />
        </Grid>

        <Grid item xs={6} md={3} lg={2}>
          <TextField
            fullWidth
            size="small"
            type="number"
            label="Score Máximo"
            value={filters.scoreMax}
            onChange={handleTextChange('scoreMax')}
            inputProps={{ min: 1, max: 7, step: 0.1 }}
            helperText="1-7"
          />
        </Grid>
      </Grid>
    </Paper>
  );
};

export default EmployeeFilterBar;
