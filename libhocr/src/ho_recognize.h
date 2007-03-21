/***************************************************************************
 *            ho_recognize.h
 *
 *  Fri Aug 12 20:13:33 2005
 *  Copyright  2005-2007  Yaacov Zamir
 *  <kzamir@walla.co.il>
 ****************************************************************************/

/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Library General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA.
 */

#ifndef HO_RECOGNIZE_H
#define HO_RECOGNIZE_H 1

#include <ho_bitmap.h>
#include <ho_objmap.h>

int
ho_recognize_hbar_up (const ho_bitmap * m_text, const ho_bitmap * m_mask,
		      double *height, double *start, double *end);

int
ho_recognize_hbar_down (const ho_bitmap * m_text,
			const ho_bitmap * m_mask, double *height,
			double *start, double *end);

int ho_recognize_vbar_right (const ho_bitmap * m_text,
			     const ho_bitmap * m_mask, double *width,
			     double *start, double *end);

int ho_recognize_vbar_left (const ho_bitmap * m_text,
			    const ho_bitmap * m_mask, double *width,
			    double *start, double *end);

int
ho_recognize_dbar_left (const ho_bitmap * m_text, const ho_bitmap * m_mask,
			double *width, double *start, double *end);

int
ho_recognize_edges_top (const ho_bitmap * m_text, const ho_bitmap * m_mask,
			int *num, int *left, int *middle, int *right);

int
ho_recognize_edges_bottom (const ho_bitmap * m_text, const ho_bitmap * m_mask,
			   int *num, int *left, int *middle, int *right);

int
ho_recognize_edges_left (const ho_bitmap * m_text, const ho_bitmap * m_mask,
			 int *num, int *top, int *middle, int *bottom);

int
ho_recognize_edges_right (const ho_bitmap * m_text, const ho_bitmap * m_mask,
			  int *num, int *top, int *middle, int *bottom);

int
ho_recognize_dimentions (const ho_bitmap * m_text, const ho_bitmap * m_mask,
			 double *height, double *width, double *start, double *end);

int
ho_recognize_array (const ho_bitmap * m_text, const ho_bitmap * m_mask,
		    double *array);

#endif /* HO_RECOGNIZE_H */
