<script setup>
import { onMounted, ref } from 'vue'
import { tccApi } from '../services/tccApi'

const students = ref([])
const cursos = ref([])
const isLoading = ref(true)
const errorMessage = ref('')
const searchQuery = ref('')

function getCursoNome(cursoId) {
  const c = cursos.value.find(c => c.id === cursoId)
  return c ? c.nome : `#${cursoId}`
}

async function loadStudents() {
  isLoading.value = true
  errorMessage.value = ''
  try {
    const params = {}
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim()
    }
    const [studentsRes, cursosRes] = await Promise.all([
      tccApi.getStudents(params),
      tccApi.getCourses(),
    ])
    students.value = studentsRes.data
    cursos.value = cursosRes.data
  } catch (error) {
    errorMessage.value = 'Não foi possível carregar os alunos. Verifique se o backend está rodando.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

function handleSearch() {
  loadStudents()
}

onMounted(loadStudents)
</script>

<template>
  <section class="page">
    <header class="page-header">
      <div>
        <h1>Alunos</h1>
        <p>Consulta de alunos cadastrados.</p>
      </div>
    </header>

    <div class="search-bar">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Buscar por nome ou matrícula..."
        @keyup.enter="handleSearch"
      />
      <button type="button" class="button-secondary" @click="handleSearch">
        Buscar
      </button>
    </div>

    <div v-if="isLoading" class="status-box">
      Carregando alunos...
    </div>

    <div v-else-if="errorMessage" class="status-box status-box-error">
      {{ errorMessage }}
    </div>

    <div v-else-if="students.length === 0" class="status-box">
      Nenhum aluno encontrado.
    </div>

    <div v-else class="table-container">
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Matrícula</th>
            <th>Curso</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="aluno in students" :key="aluno.id">
            <td>{{ aluno.nome }}</td>
            <td>{{ aluno.matricula }}</td>
            <td>{{ getCursoNome(aluno.curso) }}</td>
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
