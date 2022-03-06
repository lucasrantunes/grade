from django.db import models

class Curso(models.Model):
    nome = models.CharField(max_length=200)
    code = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    codigo_disciplina = models.CharField(max_length=15, default="")
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
    codigo_disciplina = models.CharField(max_length=15, default="")
    codigo_turma = models.CharField(max_length=5)
    enquadramento = models.IntegerField(default=1, choices=tipos_enquadramento)
    vagas_total = models.IntegerField(default=0)
    vagas_calouros = models.IntegerField(default=0)
    reserva = models.CharField(max_length=20)
    prioridade_curso = models.CharField(max_length=150)
    horario = models.CharField(max_length=150)
    professor = models.CharField(max_length=120)
    optativa = models.CharField(max_length=400)

    def __str__(self):
        return f"{self.codigo_disciplina} {self.codigo_turma}"