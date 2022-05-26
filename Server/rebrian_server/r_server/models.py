from django.db import models


class Client(models.Model):
    name = models.CharField('name', max_length=255)
    description = models.TextField('Description', max_length=255, default='no_description')
    memory_total = models.CharField('Memory total', max_length=20)
    memory_used = models.CharField('Memory used', max_length=20)
    memory_percent = models.IntegerField('Memory percent')
    cpu_cores = models.IntegerField()
    cpu_physical_cores = models.IntegerField()
    cpu_frequency_current = models.IntegerField()
    cpu_frequency_max = models.IntegerField()
    load_average_1min = models.FloatField('load average 1min')
    load_average_5min = models.FloatField('load average 5min')
    load_average_15min = models.FloatField('load average 15min')
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    client_is_active = models.BooleanField(default=True, verbose_name='Active')
    disks = models.JSONField(verbose_name='Disks')
    net_adapter = models.JSONField(verbose_name='Net Adapters')

    class Meta:
        managed = True
        verbose_name = 'Client'

    def __str__(self):
        return '%s - %s - %s' % (self.name, self.memory_total, self.cpu_frequency_max)
