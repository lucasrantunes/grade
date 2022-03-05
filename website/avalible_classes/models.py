from django.db import models

class Curso(models.model):
    nome = models.CharField(max_length=200)
    code = models.IntegerField(default=0)

class Disciplina(models.model):
    nome = models.CharField(max_length=200)
    aulas_semanais = models.IntegerField(default=0)

class Turma(models.model):
    PRESENCIAL = 1
    HIBRIDA = 2
    REMOTO = 3
    tipos_enquadramento = ((PRESENCIAL,'Presencial'), 
                            (HIBRIDA,'Hibrida'), 
                             (REMOTO,'Remoto'),
    )

    turma = models.CharField(max_length=5)
    enquadramento = models.IntegerChoices(default=1, choices=tipos_enquadramento)
    vagas_total = models.IntegerField(default=0)
    vagas_calouros = models.IntegerField(default=0)
    reserva = models.CharField(max_length=20)
    prioridade_curso = models.CharField(max_length=150)
    horario = models.CharField(max_length=150)
    professor = models.CharField(max_length=120)
    optativa = models.CharField(max_length=400)