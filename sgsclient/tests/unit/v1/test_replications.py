#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from sgsclient.tests.unit import base
from sgsclient.tests.unit.v1 import fakes

cs = fakes.FakeClient()
mock_request_return = ({}, {'replication': {'name': 'fake_name'}})


class ReplicationsTest(base.TestCaseShell):
    @mock.patch('sgsclient.client.HTTPClient.json_request')
    def test_list_replications_with_marker_limit(self, mock_request):
        mock_request.return_value = mock_request_return
        cs.replications.list(marker=1234, limit=2)
        mock_request.assert_called_with(
            'GET',
            '/replications?limit=2&marker=1234',
            headers={})

    @mock.patch('sgsclient.client.HTTPClient.json_request')
    def test_list_replications_with_sort_key_dir(self, mock_request):
        mock_request.return_value = mock_request_return
        cs.replications.list(sort_key='id', sort_dir='asc')
        mock_request.assert_called_with(
            'GET',
            '/replications?sort_dir=asc&sort_key=id',
            headers={})

    @mock.patch('sgsclient.client.HTTPClient.json_request')
    def test_list_replications_with_invalid_sort_key(self, mock_request):
        self.assertRaises(ValueError,
                          cs.replications.list, sort_key='invalid',
                          sort_dir='asc')

    @mock.patch('sgsclient.client.HTTPClient.json_request')
    def test_create_replication(self, mock_request):
        mock_request.return_value = mock_request_return
        cs.replications.create('master_volume', 'slave_volume',
                               'replication name', 'description')
        mock_request.assert_called_with(
            'POST',
            '/replications',
            data={
                'replication': {
                    'master_volume': 'master_volume',
                    'slave_volume': 'slave_volume',
                    'name': 'replication name',
                    'description': 'description'}},
            headers={})

    @mock.patch('sgsclient.client.HTTPClient.raw_request')
    def test_delete_replication(self, mock_request):
        mock_request.return_value = mock_request_return
        cs.replications.delete('1')
        mock_request.assert_called_with(
            'DELETE',
            '/replications/1',
            headers={})

    @mock.patch('sgsclient.client.HTTPClient.json_request')
    def test_create_update(self, mock_request):
        mock_request.return_value = mock_request_return
        cs.replications.update('1', name='Test name.')
        mock_request.assert_called_with(
            'PUT',
            '/replications/1',
            data={'replication': {'name': 'Test name.'}}, headers={})

    @mock.patch('sgsclient.client.HTTPClient.json_request')
    def test_show_replication(self, mock_request):
        mock_request.return_value = mock_request_return
        cs.replications.get('1')
        mock_request.assert_called_with(
            'GET',
            '/replications/1',
            headers={})

    @mock.patch('sgsclient.client.HTTPClient.json_request')
    def test_show_replication_with_headers(self, mock_request):
        mock_request.return_value = mock_request_return
        cs.replications.get('1', session_id='fake_session_id')
        mock_request.assert_called_with(
            'GET',
            '/replications/1',
            headers={'X-Configuration-Session': 'fake_session_id'})

    @mock.patch('sgsclient.client.HTTPClient.json_request')
    def test_enable_replication(self, mock_request):
        mock_request.return_value = mock_request_return
        replication_id = "1"
        cs.replications.enable(replication_id)
        mock_request.assert_called_with(
            'POST',
            '/replications/1/action',
            data={"enable": None})

    @mock.patch('sgsclient.client.HTTPClient.json_request')
    def test_disable_replication(self, mock_request):
        mock_request.return_value = mock_request_return
        replication_id = "1"
        cs.replications.disable(replication_id)
        mock_request.assert_called_with(
            'POST',
            '/replications/1/action',
            data={"disable": None})

    @mock.patch('sgsclient.client.HTTPClient.json_request')
    def test_failover_replication(self, mock_request):
        mock_request.return_value = mock_request_return
        replication_id = "1"
        cs.replications.failover(replication_id)
        mock_request.assert_called_with(
            'POST',
            '/replications/1/action',
            data={"failover": {'force': False}})

    @mock.patch('sgsclient.client.HTTPClient.json_request')
    def test_reverse_replication(self, mock_request):
        mock_request.return_value = mock_request_return
        replication_id = "1"
        cs.replications.reverse(replication_id)
        mock_request.assert_called_with(
            'POST',
            '/replications/1/action',
            data={"reverse": None})
