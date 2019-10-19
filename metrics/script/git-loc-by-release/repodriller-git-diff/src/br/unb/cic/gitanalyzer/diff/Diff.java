package br.unb.cic.gitanalyzer.diff;

import org.apache.commons.io.FilenameUtils;
import java.text.SimpleDateFormat;
import java.util.ArrayList;

import org.repodriller.domain.Commit;
import org.repodriller.domain.Modification;
import org.repodriller.persistence.PersistenceMechanism;
import org.repodriller.scm.CommitVisitor;
import org.repodriller.scm.SCMRepository;

public class Diff implements CommitVisitor {

	@Override
	public void process(SCMRepository repo, Commit commit, PersistenceMechanism writer) {
		//countLinesOfCode(repo, commit, writer);
		listCommits(repo, commit, writer);
	}

	private void countLinesOfCode(SCMRepository repo, Commit commit, PersistenceMechanism writer) {
		int added = 0;
		int removed = 0;
		for (Modification m : commit.getModifications()) {
			if (m.getFileName().endsWith(".aj") || m.getFileName().endsWith(".java") /*|| m.getFileName().endsWith(".deltaj")*/) {
				added += m.getAdded();
				removed += m.getRemoved();
			}
		}
		writer.write(commit.getHash(), added, removed);
	}

	private void listCommits(SCMRepository repo, Commit commit, PersistenceMechanism writer) {
		ArrayList<String> fileNames = new ArrayList<String>();
		for (Modification m : commit.getModifications()) {
			if (m.getFileName().endsWith(".deltaj")) {
				String fileName = FilenameUtils.getName(m.getFileName());
				fileNames.add(FilenameUtils.removeExtension(fileName));
			}
		}
		SimpleDateFormat formato = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");
		writer.write(commit.getHash(),formato.format(commit.getDate().getTime()), formatFileNames(fileNames));
	}

	private String formatFileNames(ArrayList<String> listFileNames) {
		String fileNames = "";
		int listSize = listFileNames.size() - 1;
		for (int i = 0; i <= listSize; i++) {
			if (i < listSize) {
				fileNames += listFileNames.get(i) + ", ";
			}
			else {
				fileNames += listFileNames.get(i);
			}
		}
		if (listSize == -1) {
			fileNames = "-";
		}
		return fileNames;
	}
}
