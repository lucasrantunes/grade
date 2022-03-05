from django.db import models

class Curso(models.Model):
    nome = models.CharField(max_length=200)
    code = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=200)
    aulas_semanais = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Turma(models.Model):
    PRESENCIAL = 1
    HIBRIDA = 2
    REMOTO = 3
    tipos_enquadramento = ((PRESENCIAL,'Presencial'), 
                            (HIBRIDA,'Hibrida'), 
                             (REMOTO,'Remoto'),
    )

    turma = models.CharField(max_length=5)
    enquadramento = models.IntegerField(default=1, choices=tipos_enquadramento)
    vagas_total = models.IntegerField(default=0)
    vagas_calouros = models.IntegerField(default=0)
    reserva = models.CharField(max_length=20)
    prioridade_curso = models.CharField(max_length=150)
    horario = models.CharField(max_length=150)
    professor = models.CharField(max_length=120)
    optativa = models.CharField(max_length=400)