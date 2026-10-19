from rest_framework import status
from rest_framework.test import APITestCase

from .models import UnidadeAcademica, Departamento, Curso, Aluno, Professor, TCC


class TCCApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        unidade = UnidadeAcademica.objects.create(nome="Instituto de Ciências Exatas e Tecnológicas", sigla="ICET")
        depto = Departamento.objects.create(nome="Ciência da Computação", sigla="DCC", unidade_academica=unidade)
        curso = Curso.objects.create(nome="Sistemas de Informação", sigla="SI", codigo="G014")
        cls.aluno = Aluno.objects.create(nome="Aluno Teste", matricula="202300001", curso=curso)
        cls.orientador = Professor.objects.create(nome="Prof. Orientador", departamento=depto)
        cls.membro1 = Professor.objects.create(nome="Prof. Membro 1", departamento=depto)
        cls.membro2 = Professor.objects.create(nome="Prof. Membro 2", departamento=depto)

        cls.tcc_aprovado = cls.criar_tcc("Sistema Web com Django", status_tcc="2", tipo="MONOGRAFIA")
        cls.criar_tcc("Machine Learning aplicado", status_tcc="1", tipo="ARTIGO")
        cls.criar_tcc("Automação de processos", status_tcc="1", tipo="ARTIGO")

    @classmethod
    def criar_tcc(cls, titulo, status_tcc, tipo):
        return TCC.objects.create(
            titulo=titulo,
            resumo=f"Resumo de {titulo}",
            palavras_chave="teste",
            tipo=tipo,
            idioma="PT",
            aluno=cls.aluno,
            orientador=cls.orientador,
            presidente=cls.orientador,
            primeiro_membro=cls.membro1,
            segundo_membro=cls.membro2,
            status=status_tcc,
        )

    def payload_tcc(self, **extra):
        payload = {
            "titulo": "Novo TCC",
            "resumo": "Resumo do novo TCC",
            "palavras_chave": "api, testes",
            "tipo": "RELATORIO_TECNICO",
            "idioma": "PT",
            "aluno": self.aluno.id,
            "orientador": self.orientador.id,
            "presidente": self.orientador.id,
            "primeiro_membro": self.membro1.id,
            "segundo_membro": self.membro2.id,
        }
        payload.update(extra)
        return payload

    def test_lista_tccs_com_labels_legiveis(self):
        response = self.client.get("/api/tccs/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        aprovado = next(t for t in response.data if t["id"] == self.tcc_aprovado.id)
        self.assertEqual(aprovado["status_display"], "Aprovado")
        self.assertEqual(aprovado["tipo_display"], "Monografia")

    def test_busca_por_titulo(self):
        response = self.client.get("/api/tccs/", {"search": "Django"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([t["titulo"] for t in response.data], ["Sistema Web com Django"])

    def test_cria_tcc_com_status_padrao_em_elaboracao(self):
        response = self.client.post("/api/tccs/", self.payload_tcc(), format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "0")
        self.assertEqual(response.data["status_display"], "Em Elaboração")

    def test_rejeita_tcc_sem_campos_obrigatorios(self):
        response = self.client.post("/api/tccs/", {"titulo": "Incompleto"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("aluno", response.data)
        self.assertIn("orientador", response.data)

    def test_atualiza_status_do_tcc(self):
        response = self.client.patch(f"/api/tccs/{self.tcc_aprovado.id}/", {"status": "3"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status_display"], "Reprovado")

    def test_estatisticas_agrega_por_status_tipo_e_curso(self):
        response = self.client.get("/api/tccs/estatisticas/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_geral"], 3)
        self.assertEqual(response.data["por_status"], {"Aprovado": 1, "Enviado": 2})
        self.assertEqual(response.data["por_tipo"], {"Monografia": 1, "Artigo": 2})
        self.assertEqual(response.data["por_curso"], {"Sistemas de Informação": 3})
        self.assertEqual(response.data["por_orientador"], {"Prof. Orientador": 3})
