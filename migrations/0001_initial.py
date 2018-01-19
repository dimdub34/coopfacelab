# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree.db.models
import otree_save_the_change.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(to='otree.Session', related_name='coopfacevoice_group')),
            ],
            options={
                'db_table': 'coopfacevoice_group',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_payoff', otree.db.models.CurrencyField(null=True, default=0)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_gbat_arrived', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('_gbat_grouped', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('coop_id', otree.db.models.CharField(max_length=10000, null=True)),
                ('noncoop_id', otree.db.models.CharField(max_length=10000, null=True)),
                ('left_is_coop', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])),
                ('choice_id', otree.db.models.PositiveIntegerField(choices=[(0, 'Gauche'), (1, 'Droite')], null=True)),
                ('choose_cooperator', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])),
                ('period_selected_for_pay', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])),
                ('part_payoff', otree.db.models.CurrencyField(null=True)),
                ('group', models.ForeignKey(to='coopfacevoice.Group', null=True)),
                ('participant', models.ForeignKey(to='otree.Participant', related_name='coopfacevoice_player')),
                ('session', models.ForeignKey(to='otree.Session', related_name='coopfacevoice_player')),
            ],
            options={
                'db_table': 'coopfacevoice_player',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(to='otree.Session', null=True, related_name='coopfacevoice_subsession')),
            ],
            options={
                'db_table': 'coopfacevoice_subsession',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.AddField(
            model_name='player',
            name='subsession',
            field=models.ForeignKey(to='coopfacevoice.Subsession'),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(to='coopfacevoice.Subsession'),
        ),
    ]
