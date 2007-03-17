/***************************************************************************
 *            ho_pixbuf.h
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

#ifndef HO_PIXBUF_H
#define HO_PIXBUF_H 1

#include <ho_bitmap.h>
#include <ho_objmap.h>

/* utility defines */
#define ho_pixbuf_min3(a,b,c) ((((a)<(b))&&((a)<(c))) ? (a) : (((b)<(c)) ? (b) : (c)))
#define ho_pixbuf_max3(a,b,c) ((((a)>(b))&&((a)>(c))) ? (a) : (((b)>(c)) ? (b) : (c)))

 /* hocr pixbuf set/get macros */
#define ho_pixbuf_set(m,x,y,col,val) (((m)->data)[(x)*(m)->n_channels+(y)*(m)->rowstride+(col)]=(val))
#define ho_pixbuf_get(m,x,y,col) (((m)->data)[(x)*(m)->n_channels+(y)*(m)->rowstride+(col)])

#define ho_pixbuf_get_n_channels(m) ((m)->n_channels)
#define ho_pixbuf_get_width(m) ((m)->width)
#define ho_pixbuf_get_height(m) ((m)->height)
#define ho_pixbuf_get_rowstride(m) ((m)->rowstride)
#define ho_pixbuf_get_data(m) ((m)->data)

/* hocr pixbuf: copy of gtk_pixbuf */
typedef struct
{
  unsigned char n_channels;
  int height;
  int width;
  int rowstride;
  unsigned char *data;
} ho_pixbuf;

/**
 new ho_pixbuf 
 @param n_channels number of color channels
 @param hight hight of pixbuf in pixels
 @param width width of pixbuf in pixels
 @param rowstride number of bytes in a row
 @return newly allocated ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_new (const unsigned char n_channels,
			  const int width, const int height,
			  const int rowstride);

/**
 clone ho_pixbuf
 @param m pointer to a ho_pixbuf image
 @return newly allocated gray ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_clone (const ho_pixbuf * m);

/**
 new ho_pixbuf from ho_bitmap
 @param bit_in pointer to an ho_bitmap image
 @return newly allocated gray ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_new_from_bitmap (const ho_bitmap * bit_in);

/**
 new ho_pixbuf from ho_objmap
 @param obj_in pointer to an ho_objmap image
 @param min minimal color value
 @param max maximal color value
 @return newly allocated color ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_new_from_objmap (const ho_objmap * obj_in,
				      const unsigned char min,
				      const unsigned char max);

/**
 new rgb ho_pixbuf from non rgb pixbuf
 @param pix_in pointer the original pixbuf
 @return newly allocated rgb color ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_to_rgb (const ho_pixbuf * pix_in);

/**
 free an ho_pixbuf 
 @param pix pointer to an ho_pixbuf
 @return FALSE
 */
int ho_pixbuf_free (ho_pixbuf * pix);

/**
 converts a color pixbuf to gray one
 @param pix the color ho_pixbuf
 @return newly allocated gray ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_color_to_gray (const ho_pixbuf * pix);

/**
 take the Red channel from an RGB pixbuf
 @param pix the color ho_pixbuf
 @return newly allocated gray ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_color_to_red (const ho_pixbuf * pix);

/**
 take the Green channel from an RGB pixbuf
 @param pix the color ho_pixbuf
 @return newly allocated gray ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_color_to_green (const ho_pixbuf * pix);

/**
 take the Blue channel from an RGB pixbuf
 @param pix the color ho_pixbuf
 @return newly allocated gray ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_color_to_blue (const ho_pixbuf * pix);

/**
 scale a gray pixbuf to by 2
 @param pix the input ho_pixbuf
 @return newly allocated gray ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_scale2 (const ho_pixbuf * pix);

/**
 scale a gray pixbuf to by 3
 @param pix the input ho_pixbuf
 @return newly allocated gray ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_scale3 (const ho_pixbuf * pix);

/**
 scale a gray pixbuf
 @param pix the input ho_pixbuf
 @param scale scale by this factor
 @return newly allocated gray ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_scale (const ho_pixbuf * pix, const unsigned char scale);

/**
 get the min and max values in a gray pixbuf
 @param pix gray ho_pixbuf 
 @param min a pointer to return the min 
 @param max a pointer to return the max 
 @return FALSE
 */
unsigned char
ho_pixbuf_minmax (const ho_pixbuf * pix, unsigned char *min,
		  unsigned char *max);

/**
 aplay a linear filter to a gray pixbuf 
 @param pix the input ho_pixbuf
 @return newly allocated gray ho_pixbuf
 */
ho_pixbuf *ho_pixbuf_linear_filter (const ho_pixbuf * pix);

/**
 convert a gray pixbuf to bitmap 
 @param pix the input ho_pixbuf
 @param threshold the threshold to use 0..100
 @return newly allocated gray ho_bitmap
 */
ho_bitmap *ho_pixbuf_to_bitmap (const ho_pixbuf * pix,
				unsigned char threshold);

/**
 convert a gray pixbuf to bitmap using adaptive thresholding
 @param pix the input ho_pixbuf
 @param threshold the threshold to use 0..100
 @param size block size for the adaptive steps
 @param adaptive_threshold the threshold to use for adaptive thresholding 0..100
 @return newly allocated gray ho_bitmap
 */
ho_bitmap *ho_pixbuf_to_bitmap_adaptive (const ho_pixbuf * pix,
					 unsigned char threshold,
					 unsigned char size,
					 unsigned char adaptive_threshold);

/**
 convert a gray pixbuf to bitmap using better adaptive thresholding
 @param pix the input ho_pixbuf
 @param threshold the threshold to use 0..100
 @param size block size for the adaptive steps
 @param adaptive_threshold the threshold to use for adaptive thresholding 0..100
 @return newly allocated gray ho_bitmap
 */
ho_bitmap *ho_pixbuf_to_bitmap_adaptive_fine (const ho_pixbuf *
					      pix,
					      unsigned char threshold,
					      unsigned char size,
					      unsigned char
					      adaptive_threshold);

/**
 convert a gray pixbuf to bitmap wrapper function
 @param pix_in the input ho_pixbuf
 @param scale the scale to use
 @param adaptive what type of thresholding to use
 @param threshold the threshold to use 0..100
 @param a_threshold the threshold to use for adaptive thresholding 0..100
 @return newly allocated gray ho_bitmap
 */
ho_bitmap *ho_pixbuf_to_bitmap_wrapper (const ho_pixbuf * pix_in,
					const unsigned char scale,
					const unsigned char adaptive,
					const unsigned char threshold,
					const unsigned char a_threshold);

#endif /* HO_PIXBUF_H */