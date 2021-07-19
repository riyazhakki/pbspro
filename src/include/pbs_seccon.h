/*
 * Copyright (C) 1994-2021 Altair Engineering, Inc.
 * For more information, contact Altair at www.altair.com.
 *
 * This file is part of the PBS Professional ("PBS Pro") software.
 *
 * Open Source License Information:
 *
 * PBS Pro is free software. You can redistribute it and/or modify it under the
 * terms of the GNU Affero General Public License as published by the Free
 * Software Foundation, either version 3 of the License, or (at your option) any
 * later version.
 *
 * PBS Pro is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.
 * See the GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Commercial License Information:
 *
 * For a copy of the commercial license terms and conditions,
 * go to: (http://www.pbspro.com/UserArea/agreement.html)
 * or contact the Altair Legal Department.
 *
 * Altair’s dual-license business model allows companies, individuals, and
 * organizations to create proprietary derivative works of PBS Pro and
 * distribute them - whether embedded or bundled with other software -
 * under a commercial license agreement.
 *
 * Use of Altair’s trademarks, including but not limited to "PBS™",
 * "PBS Professional®", and "PBS Pro™" and Altair’s logos is subject to Altair's
 * trademark licensing policies.
 *
 */

#ifndef	_PBS_SECCON_H
#define	_PBS_SECCON_H
#ifdef	__cplusplus
extern "C" {
#endif

int sec_get_con(void *con);
int sec_set_fdcon(int fd);
int sec_set_exec_con(void *context);
int sec_set_filecon(char *path, void *context);
int sec_reset_fscon();
int sec_get_net_conn(void *con);
int sec_set_net_conn(void *con);
int sec_should_impersonate();

void sec_set_context(void **, char *);
void sec_free_con(void *con);
void *sec_open_session(char *);
void sec_close_session(void *);
void sec_revert_con(void *ctx);

#ifdef	__cplusplus
}
#endif
#endif	/* _PBS_SECCON_H */