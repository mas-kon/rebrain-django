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


# class Disks(models.Model):
#     client = models.ForeignKey('Client', related_name='disk', verbose_name='client', on_delete=models.CASCADE)
#     device = models.CharField('Device', max_length=10)
#     total = models.IntegerField('Total volume')
#     used = models.IntegerField('Used space')
#     free = models.IntegerField('Free space')
#     fstype = models.CharField('FS type', max_length=15)
#     mountpoint = models.CharField('Mount point', max_length=5)
#
#     class Meta:
#         managed = True
#         verbose_name = 'Disk'
#
#     def __str__(self):
#         return '%s: %s' % (self.device, self.total)
#
#
# class NetAdapter(models.Model):
#     client = models.ForeignKey('Client', related_name='adapter', verbose_name='client',
#                                on_delete=models.CASCADE)
#     net_adapter_device = models.CharField('NetAdapter Name', max_length=200)
#     net_adapter_status = models.BooleanField(default=False)
#     net_adapter_mtu = models.IntegerField()
#     net_adapter_speed = models.IntegerField()
#     net_adapter_duplex = models.CharField(default='Unknown', max_length=200)
#     net_adapter_bytes_send = models.IntegerField()
#     net_adapter_bytes_recv = models.IntegerField()
#     net_adapter_errs_in = models.IntegerField()
#     net_adapter_drops_in = models.IntegerField()
#     net_adapter_errs_out = models.IntegerField()
#     net_adapter_drops_out = models.IntegerField()
#     IPv4 = models.GenericIPAddressField('IPv4', protocol='IPv4', default='0.0.0.0')
#     IPv6 = models.GenericIPAddressField('IPv6', protocol='IPv6', default='0:0:0:0:0:0:0:0')
#     MAC = models.CharField(default='00-00-00-00-00-00', max_length=17)
#
#     class Meta:
#         managed = True
#         verbose_name = 'NetAdapter'
#
#     def __str__(self):
#         return '%s: %s' % (self.net_adapter_device, self.IPv4)
