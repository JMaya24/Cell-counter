# ROI selection and Cell Counter


The study of cells in neurological research is pivotal for understanding their dynamic roles in brain health and disease. However, manual analysis of microscopic images can be tedious and subject to human error. To overcome these challenges, this project focuses on developing an automated system for selecting Regions of Interest (ROIs) and performing cell counting, akin to a digital cell counter and ROI selector.


The project involves the development of algorithms utilizing image processing techniques to manually delimit ROIs containing microglia cells within widefiel fluorescence microscopic images. These algorithms require de manual delineating of the ROIs by clicking to subsequently, by preprocessing techniques, enhance image quality and generate an automatical cell counting.


One of the disadvantages of using widefield microscopies compared to confocal microscopies is that widefield microscopies use a halogen lamp illumination system and filters to allow only the required wavelength to pass through. However, this exposes the entire sample, resulting in a halo of light that represents noise when trying to delineate foreground objects. On the other hand, confocal microscopies use a laser system that offers only the required wavelength. Furthermore, these microscopies have the advantage of having a pinhole, which allows focusing on the sample in a single z-region, resulting in cleaner acquisition. However, a disadvantage is that the acquisition time is much longer. In this case, since only cell counting was intended, the widefield microscope and preprocessing techniques were chosen to achieve high-precision counts. The system effectively isolates areas of interest containing cells while minimizing background noise. Moreover, image preprocessing techniques have improved image clarity, facilitating more precise cell counting.









![Cell-Counter](https://github.com/Maya-Arteaga/Cell-counter/assets/70504322/26f74804-52c5-4c46-b9a3-2aab257a4031)
