<script setup>
import { onMounted, ref } from 'vue'
import { tccApi } from '../services/tccApi'

const professors = ref([])
const departamentos = ref([])
const isLoading = ref(true)
const errorMessage = ref('')
const searchQuery = ref('')

function getDepartamentoSigla(deptId) {
  const d = departamentos.value.find(d => d.id === deptId)
  return d ? d.sigla : `#${deptId}`
}

async function loadProfessors() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const params = {}
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim()
    }
    const [profsRes, deptsRes] = await Promise.all([
      tccApi.getProfessors(params),
      tccApi.getDepartments(),
    ])
    professors.value = profsRes.data
    departamentos.value = deptsRes.data
  } catch (error) {
    errorMessage.value = 'Não foi possível carregar os professores. Verifique se o backend está rodando.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

function handleSearch() {
  loadProfessors()
}

onMounted(loadProfessors)
</script>

<template>
  <section class="page">
    <header class="page-header">
      <div>
        <h1>Professores</h1>
        <p>Consulta de professores cadastrados.</p>
      </div>
    </header>

    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Buscar por nome..."
        @keyup.enter="handleSearch"
      />
      <button type="button" class="button-secondary" @click="handleSearch">
        Buscar
      </button>
    </div>

    <div v-if="isLoading" class="status-box">
      Carregando professores...
    </div>

    <div v-else-if="errorMessage" class="status-box status-box-error">
      {{ errorMessage }}
    </div>

    <div v-else-if="professors.length === 0" class="status-box">
      Nenhum professor encontrado.
    </div>

    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Departamento</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="prof in professors" :key="prof.id">
            <td>{{ prof.nome }}</td>
            <td>{{ getDepartamentoSigla(prof.departamento) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<style scoped>
.search-bar {
  display: flex;
  gap: 8px;
}

.search-bar input {
  flex: 1;
  border: 1px solid #c9d4e5;
  border-radius: 8px;
  padding: 10px 14px;
  background: #ffffff;
  font: inherit;
}

.table-container {
  border: 1px solid #dfe5ee;
  border-radius: 8px;
  background: #ffffff;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 12px 16px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #667085;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #edf1f7;
}

td {
  padding: 12px 16px;
  border-bottom: 1px solid #edf1f7;
  color: #17202a;
}

tr:last-child td {
  border-bottom: 0;
}
</style>
