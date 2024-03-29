# -*- coding: utf-8 -*-
# Copyright (C) 2019 Linaro Limited
#
# Author: Milosz Wasilewski <milosz.wasilewski@linaro.org>
#
# This file is part of LAVA.
#
# LAVA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3
# as published by the Free Software Foundation
#
# LAVA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with LAVA.  If not, see <http://www.gnu.org/licenses/>.

from lava_scheduler_app.models import (
    Device,
    DeviceType,
    TestJob,
    Tag,
    Architecture,
    ProcessorFamily,
    Alias,
    Worker,
    BitWidth,
    Core,
    JobFailureTag,
)
from django.contrib.auth.models import User, Group
from django_filters.filters import ChoiceFilter

import rest_framework_filters as filters

from lava_server.compat import RelatedFilter


class GroupFilter(filters.FilterSet):
    class Meta:
        model = Group
        fields = {
            "name": ["exact", "in", "contains", "icontains", "startswith", "endswith"]
        }


class UserFilter(filters.FilterSet):
    group = RelatedFilter(GroupFilter, name="group", queryset=Group.objects.all())

    class Meta:
        model = User
        fields = {
            "username": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
            "email": ["exact", "in", "contains", "icontains", "startswith", "endswith"],
        }


class ArchitectureFilter(filters.FilterSet):
    class Meta:
        model = Architecture
        fields = {
            "name": ["exact", "in", "contains", "icontains", "startswith", "endswith"]
        }


class ProcessorFamilyFilter(filters.FilterSet):
    class Meta:
        model = ProcessorFamily
        fields = {
            "name": ["exact", "in", "contains", "icontains", "startswith", "endswith"]
        }


class AliasFilter(filters.FilterSet):
    class Meta:
        model = Alias
        fields = {
            "name": ["exact", "in", "contains", "icontains", "startswith", "endswith"]
        }


class BitWidthFilter(filters.FilterSet):
    class Meta:
        model = BitWidth
        fields = {"width": ["exact", "in"]}


class CoreFilter(filters.FilterSet):
    class Meta:
        model = Core
        fields = {
            "name": ["exact", "in", "contains", "icontains", "startswith", "endswith"]
        }


class TagFilter(filters.FilterSet):
    class Meta:
        model = Tag
        fields = {
            "name": ["exact", "in", "contains", "icontains", "startswith", "endswith"],
            "description": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
        }


class JobFailureTagFilter(filters.FilterSet):
    class Meta:
        model = JobFailureTag
        fields = {
            "name": ["exact", "in", "contains", "icontains", "startswith", "endswith"],
            "description": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
        }


class WorkerFilter(filters.FilterSet):
    health = ChoiceFilter(choices=Worker.HEALTH_CHOICES)
    state = ChoiceFilter(choices=Worker.STATE_CHOICES)

    class Meta:
        model = Worker
        fields = {
            "hostname": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
            "description": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
            "last_ping": ["exact", "lt", "gt"],
            "state": ["exact", "in"],
            "health": ["exact", "in"],
        }


class DeviceTypeFilter(filters.FilterSet):
    architecture = RelatedFilter(
        ArchitectureFilter, name="architecture", queryset=Architecture.objects.all()
    )
    processor = RelatedFilter(
        ProcessorFamilyFilter, name="processor", queryset=ProcessorFamily.objects.all()
    )
    alias = RelatedFilter(AliasFilter, name="alias", queryset=Alias.objects.all())
    bits = RelatedFilter(BitWidthFilter, name="bits", queryset=BitWidth.objects.all())
    cores = RelatedFilter(CoreFilter, name="cores", queryset=Core.objects.all())
    health_denominator = ChoiceFilter(choices=DeviceType.HEALTH_DENOMINATOR)

    class Meta:
        model = DeviceType
        fields = {
            "name": ["exact", "in", "contains", "icontains", "startswith", "endswith"],
            "cpu_model": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
            "description": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
            "health_frequency": ["exact", "in"],
            "disable_health_check": ["exact", "in"],
            "health_denominator": ["exact", "in"],
            "display": ["exact", "in"],
            "core_count": ["exact", "in"],
        }


class DeviceFilter(filters.FilterSet):
    device_type = RelatedFilter(
        DeviceTypeFilter, name="device_type", queryset=DeviceType.objects.all()
    )
    physical_owner = RelatedFilter(
        UserFilter, name="physical_owner", queryset=User.objects.all()
    )
    physical_group = RelatedFilter(
        GroupFilter, name="physical_group", queryset=Group.objects.all()
    )
    tags = RelatedFilter(TagFilter, name="tags", queryset=Tag.objects.all())
    last_health_report_job = RelatedFilter(
        "TestJobFilter",
        name="last_health_report_job",
        queryset=TestJob.objects.filter(health_check=True),
    )
    worker_host = RelatedFilter(
        WorkerFilter, name="worker_host", queryset=Worker.objects.all()
    )
    health = ChoiceFilter(choices=Device.HEALTH_CHOICES)
    state = ChoiceFilter(choices=Device.STATE_CHOICES)

    class Meta:
        model = Device
        fields = {
            "hostname": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
            "device_version": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
            "description": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
            "state": ["exact", "in"],
            "health": ["exact", "in"],
        }


class TestJobFilter(filters.FilterSet):
    requested_device_type = RelatedFilter(
        DeviceTypeFilter,
        name="requested_device_type",
        queryset=DeviceType.objects.all(),
    )
    actual_device = RelatedFilter(
        DeviceFilter, name="actual_device", queryset=Device.objects.all()
    )
    tags = RelatedFilter(TagFilter, name="tags", queryset=Tag.objects.all())
    viewing_groups = RelatedFilter(
        GroupFilter, name="viewing_groups", queryset=Group.objects.all()
    )
    submitter = RelatedFilter(UserFilter, name="submitter", queryset=User.objects.all())
    failure_tags = RelatedFilter(
        JobFailureTagFilter, name="failure_tags", queryset=JobFailureTag.objects.all()
    )
    health = ChoiceFilter(choices=TestJob.HEALTH_CHOICES)
    state = ChoiceFilter(choices=TestJob.STATE_CHOICES)

    class Meta:
        model = TestJob
        fields = {
            "submit_time": ["exact", "lt", "gt"],
            "start_time": ["exact", "lt", "gt"],
            "end_time": ["exact", "lt", "gt"],
            "health_check": ["exact"],
            "target_group": ["exact", "in", "contains", "icontains", "startswith"],
            "state": ["exact", "in"],
            "health": ["exact", "in"],
            "priority": ["exact", "in"],
            "definition": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
            "original_definition": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
            "multinode_definition": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
            ],
            "failure_comment": [
                "exact",
                "in",
                "contains",
                "icontains",
                "startswith",
                "endswith",
                "isnull",
            ],
        }
