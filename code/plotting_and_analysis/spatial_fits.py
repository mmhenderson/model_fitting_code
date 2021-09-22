import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
import numpy as np
import os

from plotting_and_analysis.analysis_utils import get_roi_info

def plot_spatial_rf_circles(subject, fitting_type, out, cc_cutoff = 0.20, screen_eccen_deg = 8.4, fig_save_folder = None):

    """
    Make a plot for each ROI showing the visual field coverage of pRFs in that ROI: 
    each circle is a voxel with the size of the circle indicating the pRF's size (1 SD)
    """

    pp=0
    best_models_deg = out['best_params'][0] * screen_eccen_deg
    if len(best_models_deg.shape)==2:
        best_models_deg = np.expand_dims(best_models_deg, axis=1)
        
#     best_ecc_deg, best_angle_deg, best_size_deg = get_prf_pars_deg(out, screen_eccen_deg)    

    roi_labels_retino, roi_labels_categ, ret_group_inds, categ_group_inds, ret_group_names, categ_group_names, \
        n_rois_ret, n_rois_categ, n_rois = get_roi_info(subject, out)
    
    val_cc = out['val_cc'][:,0]

    plt.figure(figsize=(24,18))

    npy = int(np.ceil(np.sqrt(n_rois)))
    npx = int(np.ceil(n_rois/npy))

    for rr in range(n_rois):

        if rr<n_rois_ret:
            inds_this_roi = np.isin(roi_labels_retino, ret_group_inds[rr])
            rname = ret_group_names[rr]
        else:
            inds_this_roi = np.isin(roi_labels_categ, categ_group_inds[rr-n_rois_ret])
            rname = categ_group_names[rr-n_rois_ret]

        abv_thresh = val_cc>cc_cutoff
        inds2use = np.where(np.logical_and(inds_this_roi, abv_thresh))[0]

        plt.subplot(npx,npy,rr+1)
        ax = plt.gca()

        for vi, vidx in enumerate(inds2use):

            plt.plot(best_models_deg[vidx,pp,0], best_models_deg[vidx,pp,1],'.',color='k')
            circ = matplotlib.patches.Circle((best_models_deg[vidx,pp,0], best_models_deg[vidx,pp,1]), best_models_deg[vidx,pp,2], 
                                             color = [0.8, 0.8, 0.8], fill=False)
            ax.add_artist(circ)

        plt.axis('square')

        plt.xlim([-screen_eccen_deg, screen_eccen_deg])
        plt.ylim([-screen_eccen_deg, screen_eccen_deg])
        plt.xticks(np.arange(-8,9,4))
        plt.yticks(np.arange(-8,9,4))
        if rr==n_rois-5:
            plt.xlabel('x coord (deg)')
            plt.ylabel('y coord (deg)')
        else:
            plt.xticks([])
            plt.yticks([])
        plt.title('%s (%d vox)'%(rname, len(inds2use)))

    plt.suptitle('pRF estimates\nshowing all voxels with corr > %.2f\nS%02d, %s'%(cc_cutoff, subject, fitting_type));

    if fig_save_folder is not None:
        plt.savefig(os.path.join(fig_save_folder,'spatial_prf_distrib.pdf'))
        plt.savefig(os.path.join(fig_save_folder,'spatial_prf_distrib.png'))


def plot_size_vs_eccen(subject, fitting_type,out, cc_cutoff=0.2, screen_eccen_deg = 8.4, fig_save_folder=None ):
    """
    Create a scatter plot for each ROI, showing the size of each voxel's best pRF estimate versus its eccentricity.
    """

    size_lims = screen_eccen_deg*np.array([0, 0.5])
    eccen_lims = [-1, screen_eccen_deg]
    
    best_ecc_deg, best_angle_deg, best_size_deg = get_prf_pars_deg(out, screen_eccen_deg)
    
    roi_labels_retino, roi_labels_categ, ret_group_inds, categ_group_inds, ret_group_names, categ_group_names, \
        n_rois_ret, n_rois_categ, n_rois = get_roi_info(subject, out)
    
    val_cc = out['val_cc'][:,0]
    
    npx = int(np.ceil(np.sqrt(n_rois)))
    npy = int(np.ceil(n_rois/npx))
    
    plt.figure(figsize=(24,20))

    for rr in range(n_rois):

        if rr<n_rois_ret:
            inds_this_roi = np.isin(roi_labels_retino, ret_group_inds[rr])
            rname = ret_group_names[rr]
        else:
            inds_this_roi = np.isin(roi_labels_categ, categ_group_inds[rr-n_rois_ret])
            rname = categ_group_names[rr-n_rois_ret]

        abv_thresh = val_cc>cc_cutoff
        inds2use = np.where(np.logical_and(inds_this_roi, abv_thresh))[0]

        plt.subplot(npx,npy,rr+1)
        ax = plt.gca()

        plt.plot(best_ecc_deg[inds2use], best_size_deg[inds2use], '.')

        plt.xlim(eccen_lims)
        plt.ylim(size_lims)
        if rr==n_rois-4:
            plt.xlabel('eccen (deg)')
            plt.ylabel('size (deg)')
        else:
            plt.xticks([])
            plt.yticks([])

        plt.title('%s (%d vox)'%(rname, len(inds2use)))

    plt.suptitle('pRF estimates\nshowing all voxels with corr > %.2f\nS%02d, %s'%(cc_cutoff, subject, fitting_type))
    
    if fig_save_folder is not None:
        plt.savefig(os.path.join(fig_save_folder,'size_vs_eccen.png'))
        plt.savefig(os.path.join(fig_save_folder,'size_vs_eccen.pdf'))
        
        

def plot_prf_stability_partial_versions(subject, out, cc_cutoff = 0.2, screen_eccen_deg = 8.4, fig_save_folder = None):
    
    plt.figure(figsize=(24,18));

    best_models_partial_deg = out['best_params'][0]*screen_eccen_deg
    n_partial_models = best_models_partial_deg.shape[1]
    val_cc = out['val_cc'][:,0]
    abv_thresh = val_cc>cc_cutoff   

    vox2plot = np.argsort(val_cc)[-20:-1]
    colors = cm.hsv(np.linspace(0,1,len(vox2plot)+1))

    for pp in range(n_partial_models):

        plt.subplot(4,4,pp+1)
        ax = plt.gca()

        for vi, vidx in enumerate(vox2plot):
    #         if vi>1: 
    #             break

            plt.plot(best_models_partial_deg[vidx,pp,0], best_models_partial_deg[vidx,pp,1],'.',color='k')
            circ = matplotlib.patches.Circle((best_models_partial_deg[vidx,pp,0], best_models_partial_deg[vidx,pp,1]), \
                                             best_models_partial_deg[vidx,pp,2], color = colors[vi,:], fill=False)
            ax.add_artist(circ)

        plt.axis('square')

        plt.xlim([-screen_eccen_deg, screen_eccen_deg])
        plt.ylim([-screen_eccen_deg, screen_eccen_deg])
        plt.xticks(np.arange(-8,9,4))
        plt.yticks(np.arange(-8,9,4))
        if pp==n_partial_models-4:
            plt.xlabel('x coord (deg)')
            plt.ylabel('y coord (deg)')

        plt.title('partial model version %d'%pp)

    # plt.suptitle('X coordinate of pRF fits')
    # plt.suptitle('Y coordinate of pRF fits')
    plt.suptitle('Stability of pRF fits for various versions of model (holding out sets of features)\nBest 20 voxels')

    if fig_save_folder:
        plt.savefig(os.path.join(fig_save_folder,'prf_stability_holdout.pdf'))
        plt.savefig(os.path.join(fig_save_folder,'prf_stability_holdout.png'))

        
        
def get_prf_pars_deg(out, screen_eccen_deg=8.4):
    """
    Convert the saved estimates of prf position/sd into eccentricity, angle, etc in degrees.
    """
    if len(out['best_params'])==7:
        best_models, weights, bias, features_mt, features_st, best_model_inds, _ = out['best_params']
    else:
        best_models, weights, bias, features_mt, features_st, best_model_inds = out['best_params']
    best_models_deg = best_models * screen_eccen_deg
    if len(best_models_deg.shape)==2:
        best_models_deg = np.expand_dims(best_models_deg, axis=1)
    pp=0
    best_ecc_deg  = np.sqrt(np.square(best_models_deg[:,pp,0]) + np.square(best_models_deg[:,pp,1]))
    best_angle_deg  = np.mod(np.arctan2(best_models_deg[:,pp,1], best_models_deg[:,pp,0])*180/np.pi, 360)
    best_size_deg = best_models_deg[:,pp,2]
    
    return best_ecc_deg, best_angle_deg, best_size_deg